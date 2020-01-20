from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.response import Response

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .models import Fund
from users.permissions import IsAdminUserOrOwner
from .serializers import FundSerializer
from .renderers import FundJSONRenderer, FundsJSONRenderer


class CreateFundAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FundSerializer
    renderer_classes = (FundJSONRenderer,)

    def post(self, request):
        fund = request.data.get('fund', {})

        if not request.user.is_staff:
            fund['user'] = {'id': request.user.pk}

        serializer = self.serializer_class(
            data=fund,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FundByIdAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminUserOrOwner,)
    serializer_class = FundSerializer
    renderer_classes = (FundJSONRenderer,)

    def get_object(self):
        obj = get_object_or_404(Fund, pk=self.kwargs['id'])

        self.check_object_permissions(self.request, obj.user)

        return obj

    def retrieve(self, request, *args, **kwargs):
        fund = self.get_object()

        serializer = self.serializer_class(
            fund,
            context={'request': request}  # required by url field
        )

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        fund = self.get_object()
        data = request.data.get('fund', {})

        serializer = self.serializer_class(
            fund,
            data=data,
            partial=True,
            context={'request': request}  # required by url field
        )

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        fund = self.get_object()
        data = request.data.get('fund', {})

        serializer = self.serializer_class(fund, data=data)

        serializer.delete(fund)

        return Response({}, status=status.HTTP_200_OK)


class ListFundsAPIView(RetrieveAPIView):
    permission_classes = (IsAdminUserOrOwner,)
    serializer_class = FundSerializer
    renderer_classes = (FundsJSONRenderer,)

    def get_queryset(self, request):
        user = None

        # Get query parameters
        filters = request.query_params.getlist('filters')
        filters = {f.split(':')[0]: f.split(':')[1] for f in filters if len(f.split(':')) == 2}
        filters = {**{'user_id': None, 'code': None, 'name': None}, **filters}

        # Convert parameter values
        if filters['user_id']:
            filters['user_id'] = int(filters['user_id']) if filters['user_id'].isdigit() else -1

        if filters['code']:
            filters['code'] = (filters['code'].split(' ') + [None])[:2]

        # Check user permissions
        if not request.user.is_staff:
            if not filters['user_id'] or filters['user_id'] == request.user.pk:
                user = request.user
            self.check_object_permissions(request, user)

        # Check if user parameter exists
        if not user and filters['user_id']:
            user = get_object_or_404(get_user_model(), pk=filters['user_id'])

        # Select proper dataset based on user
        data = Fund.objects.filter(user=user) if user else Fund.objects.all()

        # Filter data
        filtered_data = []
        for row in data:
            if not filters['code'] or (
                (not filters['code'][0] or filters['code'][0] <= row.code) and
                (not filters['code'][1] or filters['code'][1] >= row.code)
            ):
                if not filters['name'] or filters['name'] in row.name:
                    filtered_data.append(row)

        return filtered_data

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset(request)

        serializer = self.serializer_class(
            queryset,
            many=True,
            context={'request': request}  # required by url field
        )

        return Response({'objects': serializer.data}, status=status.HTTP_200_OK)
