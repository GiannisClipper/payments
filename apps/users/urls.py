from django.urls import path

from .views import (
    SignupAPIView,
    SigninAPIView,
)

app_name = 'users'

urlpatterns = [
    path('api/signup/', SignupAPIView.as_view(), name='signup'),  # POST
    path('api/signin/', SigninAPIView.as_view(), name='signin'),  # POST
]
