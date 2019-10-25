from django.urls import path

from .views import (
    CreateFundAPIView,
    FundByIdAPIView,
    ListFundsAPIView,
)

app_name = 'funds'

urlpatterns = [
    path('', CreateFundAPIView.as_view(), name='root'),  # POST
    path('<int:id>/', FundByIdAPIView.as_view(), name='by-id'),  # GET, PATCH, DELETE
    path('list', ListFundsAPIView.as_view(), name='list'),  # GET
]
