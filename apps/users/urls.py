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
    path(  # POST
        'signup/', SignupAPIView.as_view(), name='signup'
    ),
    path(  # POST
        'signin/', SigninAPIView.as_view(), name='signin'
    ),

    path(  # POST, GET, PATCH, DELETE
        'current/', CurrentUserAPIView.as_view(), name='current'
    ),
    path(  # POST, GET, PATCH, DELETE
        '<int:id>/', UserByIdAPIView.as_view(), name='by-id'
    ),

    path(  # GET
        'all-list/', AllUsersAPIView.as_view(), name='all-list'
    ),

    path(  # GET
        'admin-list/', AdminUsersAPIView.as_view(), name='admin-list'
    ),
    path(  # GET
        'no-admin-list/', NoAdminUsersAPIView.as_view(), name='no-admin-list'
    ),

    path(  # GET
        'active-list/', ActiveUsersAPIView.as_view(), name='active-list'
    ),
    path(  # GET
        'no-active-list/', NoActiveUsersAPIView.as_view(),
        name='no-active-list'
    ),
]
