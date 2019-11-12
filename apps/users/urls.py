from django.urls import path

from .views import (
    SignupAPIView, SigninAPIView,

    CurrentUserAPIView, UserByIdAPIView,

    AllUsersAPIView,

    AdminUsersAPIView, NoAdminUsersAPIView,

    ActiveUsersAPIView, NoActiveUsersAPIView,
)

app_name = 'users'

urlpatterns = [
    path('signup/', SignupAPIView.as_view(), name='signup'),  # POST
    path('signin/', SigninAPIView.as_view(), name='signin'),  # POST

    path('<int:id>/', UserByIdAPIView.as_view(), name='by-id'),  # POST, GET, PATCH, DELETE
    path('current/', CurrentUserAPIView.as_view(), name='current'),  # POST, GET, PATCH, DELETE

    path('all-list/', AllUsersAPIView.as_view(), name='all-list'),  # GET
    path('admin-list/', AdminUsersAPIView.as_view(), name='admin-list'),  # GET
    path('no-admin-list/', NoAdminUsersAPIView.as_view(), name='no-admin-list'),  # GET
    path('active-list/', ActiveUsersAPIView.as_view(), name='active-list'),  # GET
    path('no-active-list/', NoActiveUsersAPIView.as_view(), name='no-active-list'),  # GET
]
