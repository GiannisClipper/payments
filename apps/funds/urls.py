from django.urls import path

from .views import (
    CreateFundAPIView,
    FundByIdAPIView,
)

app_name = 'funds'

urlpatterns = [
    path(  # POST
        '', CreateFundAPIView.as_view(), name='root'
    ),
    path(  # GET, PATCH, DELETE
        '<int:id>/', FundByIdAPIView.as_view(), name='by-id'
    ),
]