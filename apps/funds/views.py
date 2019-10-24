from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from .models import Fund
from users.permissions import IsAdminUserOrOwner
from .serializers import FundSerializer
from .renderers import Fund2JSONRenderer


class CreateFundAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FundSerializer
    renderer_classes = (Fund2JSONRenderer,)

    def post(self, request):
        fund = request.data.get('fund', {})

        if not request.user.is_staff:
            fund['user'] = request.user.pk

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
    renderer_classes = (Fund2JSONRenderer,)

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
