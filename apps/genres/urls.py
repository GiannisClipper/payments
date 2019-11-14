from django.urls import path

from .views import (
    CreateGenreAPIView,
    GenreByIdAPIView,
    ListGenresAPIView,
)

app_name = 'genres'

urlpatterns = [
    path('', CreateGenreAPIView.as_view(), name='root'),  # POST
    path('<int:id>/', GenreByIdAPIView.as_view(), name='by-id'),  # GET, PATCH, DELETE
    path('list', ListGenresAPIView.as_view(), name='list'),  # GET
]
