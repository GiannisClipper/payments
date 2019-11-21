from django.urls import path

from .views import (
    CreatePaymentAPIView,
    PaymentByIdAPIView,
    ListPaymentsAPIView,
)

app_name = 'payments'

urlpatterns = [
    path('', CreatePaymentAPIView.as_view(), name='root'),  # POST
    path('<int:id>/', PaymentByIdAPIView.as_view(), name='by-id'),  # GET, PATCH, DELETE
    path('list', ListPaymentsAPIView.as_view(), name='list'),  # GET
]
