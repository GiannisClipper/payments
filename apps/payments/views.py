from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.response import Response

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .models import Payment
from users.permissions import IsAdminUserOrOwner
from .serializers import PaymentSerializer
from .renderers import PaymentJSONRenderer, PaymentsJSONRenderer


class CreatePaymentAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PaymentSerializer
    renderer_classes = (PaymentJSONRenderer,)

    def post(self, request):
        payment = request.data.get('payment', {})

        if not request.user.is_staff:
            payment['user'] = {'id': request.user.pk}

        serializer = self.serializer_class(
            data=payment,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PaymentByIdAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminUserOrOwner,)
    serializer_class = PaymentSerializer
    renderer_classes = (PaymentJSONRenderer,)

    def get_object(self):
        obj = get_object_or_404(Payment, pk=self.kwargs['id'])

        self.check_object_permissions(self.request, obj.user)

        return obj

    def retrieve(self, request, *args, **kwargs):
        payment = self.get_object()

        serializer = self.serializer_class(
            payment,
            context={'request': request}  # required by url field
        )

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        payment = self.get_object()
        data = request.data.get('payment', {})

        if 'user' not in data:
            data['user'] = {'id': payment.user.pk}  # to validate payment.user==genre/fund.user

        serializer = self.serializer_class(
            payment,
            data=data,
            partial=True,
            context={'request': request}  # required by url field
        )

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        payment = self.get_object()
        data = request.data.get('payment', {})

        serializer = self.serializer_class(payment, data=data)

        serializer.delete(payment)

        return Response({}, status=status.HTTP_200_OK)


class ListPaymentsAPIView(RetrieveAPIView):
    permission_classes = (IsAdminUserOrOwner,)
    serializer_class = PaymentSerializer
    renderer_classes = (PaymentsJSONRenderer,)

    def get_queryset(self, request):
        user = None
        user_id = request.query_params.get('user_id', None)

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
            data = Payment.objects.filter(user=user)
        else:
            data = Payment.objects.all()

        return data

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset(request)

        serializer = self.serializer_class(
            queryset,
            many=True,
            context={'request': request}  # required by url field
        )

        return Response({'objects': serializer.data}, status=status.HTTP_200_OK)
