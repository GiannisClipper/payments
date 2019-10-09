from django.urls import path

from .views import (
    SignupAPIView,
    SigninAPIView,
    CurrentUserAPIView,
    UserByIdAPIView,
    AllUsersAPIView,
)

app_name = 'users'

urlpatterns = [
    path('signup/', SignupAPIView.as_view(), name='signup'),  # POST
    path('signin/', SigninAPIView.as_view(), name='signin'),  # POST

    path('current/', CurrentUserAPIView.as_view(), name='current'),
    # POST, GET, PATCH, DELETE

    path('<int:id>/', UserByIdAPIView.as_view(), name='byid'),
    # POST, GET, PATCH, DELETE

    path('list/', AllUsersAPIView.as_view(), name='list'),  # GET
]
