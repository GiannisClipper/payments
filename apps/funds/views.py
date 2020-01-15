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
        user_id = request.query_params.get('user_id', None)
        f_name = request.query_params.get('name', None)

        # Convert parameters
        try: user_id = None if not user_id else int(user_id)  # noqa: E701
        except Exception: user_id = -1  # noqa: E701

        # Check permissions
        if not request.user.is_staff:
            if not user_id or user_id == request.user.pk:
                user = request.user
            self.check_object_permissions(request, user)

        # Check if parameter exists
        if not user and user_id:
            user = get_object_or_404(get_user_model(), pk=user_id)

        if user:
            data = Fund.objects.filter(user=user)
        else:
            data = Fund.objects.all()

        if f_name:
            data = [x for x in data if f_name in x.name]

        return data

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset(request)

        serializer = self.serializer_class(
            queryset,
            many=True,
            context={'request': request}  # required by url field
        )

        return Response({'objects': serializer.data}, status=status.HTTP_200_OK)
