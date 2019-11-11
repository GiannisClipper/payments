from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView  # , RetrieveAPIView
from rest_framework.response import Response

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .models import Genre
from users.permissions import IsAdminUserOrOwner
from .serializers import GenreSerializer
from .renderers import GenreJSONRenderer  # , GenresJSONRenderer


class CreateGenreAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = GenreSerializer
    renderer_classes = (GenreJSONRenderer,)

    def post(self, request):
        genre = request.data.get('genre', {})

        if not request.user.is_staff:
            genre['user'] = request.user.pk

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
        
        if not 'user' in data.items():
            data['user'] = genre.user  # to validate genre.user == genre.fund.user

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
