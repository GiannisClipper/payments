from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView, \
                                    RetrieveAPIView

from django.shortcuts import get_object_or_404

from .models import User
from .serializers import SignupSerializer, SigninSerializer  # , UserSerializer
from .renderers import UserJSONRenderer  # , UsersJSONRenderer


class SignupAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = SignupSerializer
    ### renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        user = request.data.get('user', {})

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        ### return Response(serializer.data, status=status.HTTP_201_CREATED)

        rendered_data = UserJSONRenderer().render(serializer.data)
        return Response(rendered_data, status=status.HTTP_201_CREATED)


class SigninAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = SigninSerializer
    ### renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        user = request.data.get('user', {})

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        ### return Response(serializer.data, status=status.HTTP_200_OK)

        rendered_data = UserJSONRenderer().render(serializer.data)
        return Response(rendered_data, status=status.HTTP_200_OK)
