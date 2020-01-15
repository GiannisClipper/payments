from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.response import Response

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .models import Genre
from users.permissions import IsAdminUserOrOwner
from .serializers import GenreSerializer
from .renderers import GenreJSONRenderer, GenresJSONRenderer


class CreateGenreAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = GenreSerializer
    renderer_classes = (GenreJSONRenderer,)

    def post(self, request):
        genre = request.data.get('genre', {})

        if not request.user.is_staff:
            genre['user'] = {'id': request.user.pk}

        serializer = self.serializer_class(
            data=genre,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GenreByIdAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminUserOrOwner,)
    serializer_class = GenreSerializer
    renderer_classes = (GenreJSONRenderer,)

    def get_object(self):
        obj = get_object_or_404(Genre, pk=self.kwargs['id'])

        self.check_object_permissions(self.request, obj.user)

        return obj

    def retrieve(self, request, *args, **kwargs):
        genre = self.get_object()

        serializer = self.serializer_class(
            genre,
            context={'request': request}  # required by url field
        )

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        genre = self.get_object()
        data = request.data.get('genre', {})

        if 'user' not in data:
            data['user'] = {'id': genre.user.pk}  # to validate genre.user == genre.fund.user

        serializer = self.serializer_class(
            genre,
            data=data,
            partial=True,
            context={'request': request}  # required by url field
        )

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        genre = self.get_object()
        data = request.data.get('genre', {})

        serializer = self.serializer_class(genre, data=data)

        serializer.delete(genre)

        return Response({}, status=status.HTTP_200_OK)


class ListGenresAPIView(RetrieveAPIView):
    permission_classes = (IsAdminUserOrOwner,)
    serializer_class = GenreSerializer
    renderer_classes = (GenresJSONRenderer,)

    def get_queryset(self, request):
        user = None
        user_id = request.query_params.get('user_id', None)
        f_name = request.query_params.get('name', None)

        # Convert parameters
        try: user_id = None if not user_id else int(user_id)  # noqa: E701
        except Exception: user_id = -1  # noqa: E701

        # Check permissions
        if not request.user.is_staff:
            if not user_id or user_id == request.user.pk:
                user = request.user
            self.check_object_permissions(request, user)

        # Check if parameter exists
        if not user and user_id:
            user = get_object_or_404(get_user_model(), pk=user_id)

        if user:
            data = Genre.objects.filter(user=user)
        else:
            data = Genre.objects.all()

        if f_name:
            data = [x for x in data if f_name in x.name]

        return data

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset(request)

        serializer = self.serializer_class(
            queryset,
            many=True,
            context={'request': request}  # required by url field
        )

        return Response({'objects': serializer.data}, status=status.HTTP_200_OK)
