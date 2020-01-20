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

        # Get query parameters
        filters = request.query_params.getlist('filters')
        filters = {f.split(':')[0]: f.split(':')[1] for f in filters if len(f.split(':')) == 2}
        filters = {**{
            'user_id': None,
            'code': None,
            'name': None,
            'is_incoming': None,
            'fund_id': None
        }, **filters}

        # Convert parameter values
        if filters['user_id']:
            filters['user_id'] = int(filters['user_id']) if filters['user_id'].isdigit() else -1

        if filters['code']:
            filters['code'] = (filters['code'].split(' ') + [None])[:2]

        if filters['is_incoming']:
            filters['is_incoming'] = {'true': True, 'false': False}.get(filters['is_incoming'].lower(), None)  # noqa: E501

        if filters['fund_id']:
            filters['fund_id'] = int(filters['fund_id'])

        # Check user permissions
        if not request.user.is_staff:
            if not filters['user_id'] or filters['user_id'] == request.user.pk:
                user = request.user
            self.check_object_permissions(request, user)

        # Check if user parameter exists
        if not user and filters['user_id']:
            user = get_object_or_404(get_user_model(), pk=filters['user_id'])

        # Select proper dataset based on user
        data = Genre.objects.filter(user=user) if user else Genre.objects.all()

        # Filter data
        filtered_data = []
        for row in data:
            if not filters['code'] or (
                (not filters['code'][0] or filters['code'][0] <= row.code) and
                (not filters['code'][1] or filters['code'][1] >= row.code)
            ):
                if not filters['name'] or filters['name'] in row.name:
                    if not filters['is_incoming'] or filters['is_incoming'] == row.is_incoming:
                        if not filters['fund_id'] or filters['fund_id'] == row.fund.id:
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
