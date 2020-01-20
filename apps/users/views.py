from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView, RetrieveAPIView

from django.shortcuts import get_object_or_404

from .models import User
from .permissions import IsAdminUserOrOwner
from .serializers import SignupSerializer, SigninSerializer, UserSerializer
from .renderers import UserJSONRenderer, UsersJSONRenderer


class SignupAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = SignupSerializer
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SigninAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = SigninSerializer
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CurrentUserAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    renderer_classes = (UserJSONRenderer,)

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()

        serializer = self.serializer_class(
            user,
            context={'request': request}  # required by url field
        )

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        data = request.data.get('user', {})

        serializer = self.serializer_class(
            user,
            data=data,
            partial=True,
            context={'request': request}  # required by url field
        )

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        data = request.data.get('user', {})

        serializer = self.serializer_class(user, data=data)

        serializer.delete(user)

        return Response({}, status=status.HTTP_200_OK)


class UserByIdAPIView(CurrentUserAPIView):
    permission_classes = (IsAdminUserOrOwner,)

    def get_object(self):
        obj = get_object_or_404(User, pk=self.kwargs['id'])
        self.check_object_permissions(self.request, obj)
        return obj


class AllUsersAPIView(RetrieveAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = UserSerializer
    renderer_classes = (UsersJSONRenderer,)

    def get_queryset(self, request):

        # Get query parameters
        filters = request.query_params.getlist('filters')
        filters = {f.split(':')[0]: f.split(':')[1] for f in filters if len(f.split(':')) == 2}
        filters = {**{'username': None, 'email': None}, **filters}

        data = User.objects.all()

        # Filter data
        filtered_data = []
        for row in data:
            if not filters['username'] or filters['username'] in row.username:
                if not filters['email'] or filters['email'] in row.email:
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


class AdminUsersAPIView(AllUsersAPIView):

    def get_queryset(self, request):
        return User.objects.filter(is_staff=True)


class NoAdminUsersAPIView(AllUsersAPIView):

    def get_queryset(self, request):
        return User.objects.filter(is_staff=False)


class ActiveUsersAPIView(AllUsersAPIView):

    def get_queryset(self, request):
        return User.objects.filter(is_active=True)


class NoActiveUsersAPIView(AllUsersAPIView):

    def get_queryset(self, request):
        return User.objects.filter(is_active=False)
