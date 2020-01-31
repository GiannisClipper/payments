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

from datetime import datetime


class CreatePaymentAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PaymentSerializer
    renderer_classes = (PaymentJSONRenderer,)

    def post(self, request):
        payment = request.data.get('payment', {})

        if not request.user.is_staff:
            payment['user'] = {'id': request.user.pk}

        # An `incoming` value is necessary for UniqueTogether validation
        payment['incoming'] = float(payment['incoming']) if payment.get('incoming', None) else 0

        # An `outgoing` value is necessary for UniqueTogether validation
        payment['outgoing'] = float(payment['outgoing']) if payment.get('outgoing', None) else 0

        # A `remarks` value is necessary for UniqueTogether validation
        if not payment.get('remarks', None):
            payment['remarks'] = ''

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

        # Get query parameters
        filters = request.query_params.getlist('filters')
        filters = {f.split(':')[0]: f.split(':')[1] for f in filters if len(f.split(':')) == 2}
        filters = {**{
            'user_id': None,
            'date': None,
            'genre_id': None,
            'incoming': None,
            'outgoing': None,
            'remarks': None,
            'fund_id': None
        }, **filters}

        # Convert parameter values
        if filters['user_id']:
            filters['user_id'] = int(filters['user_id']) if filters['user_id'].isdigit() else -1

        if filters['date']:
            filters['date'] = (filters['date'].split(' ') + [None])[:2]
            filters['date'][0] = datetime.strptime(filters['date'][0], '%d-%m-%Y').date() if filters['date'][0] else None  # noqa: E501
            filters['date'][1] = datetime.strptime(filters['date'][1], '%d-%m-%Y').date() if filters['date'][1] else None  # noqa: E501

        if filters['incoming']:
            filters['incoming'] = (filters['incoming'].split(' ') + [None])[:2]
            filters['incoming'][0] = float(filters['incoming'][0]) if filters['incoming'][0] else None  # noqa: E501
            filters['incoming'][1] = float(filters['incoming'][1]) if filters['incoming'][1] else None  # noqa: E501

        if filters['outgoing']:
            filters['outgoing'] = (filters['outgoing'].split(' ') + [None])[:2]
            filters['outgoing'][0] = float(filters['outgoing'][0]) if filters['outgoing'][0] else None  # noqa: E501
            filters['outgoing'][1] = float(filters['outgoing'][1]) if filters['outgoing'][1] else None  # noqa: E501

        if filters['genre_id']:
            filters['genre_id'] = int(filters['genre_id'])

        if filters['fund_id']:
            filters['fund_id'] = int(filters['fund_id'])

        # Check user permissions
        if not request.user.is_staff:
            if not filters['user_id'] or filters['user_id'] == request.user.pk:
                user = request.user
            self.check_object_permissions(request, user)

        # Check if user parameter exists
        if not user and filters['user_id']:
            user = get_object_or_404(get_user_model(), pk=filters['user_id'])

        # Select proper dataset based on user
        data = Payment.objects.filter(user=user) if user else Payment.objects.all()

        # Filter data
        filtered_data = []
        for row in data:
            if not filters['date'] or (
                (not filters['date'][0] or filters['date'][0] <= row.date) and
                (not filters['date'][1] or filters['date'][1] >= row.date)
            ):
                if not filters['incoming'] or (
                    (not filters['incoming'][0] or filters['incoming'][0] <= row.incoming) and
                    (not filters['incoming'][1] or filters['incoming'][1] >= row.incoming)
                ):
                    if not filters['outgoing'] or (
                        (not filters['outgoing'][0] or filters['outgoing'][0] <= row.outgoing) and  # noqa: E501
                        (not filters['outgoing'][1] or filters['outgoing'][1] >= row.outgoing)
                    ):
                        if not filters['remarks'] or filters['remarks'] in row.remarks:
                            if not filters['genre_id'] or filters['genre_id'] == row.genre.id:
                                if not filters['fund_id'] or filters['fund_id'] == row.fund.id:
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
