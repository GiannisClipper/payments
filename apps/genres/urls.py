from django.urls import path

from .views import (
    CreateGenreAPIView,
    GenreByIdAPIView,
)
#    ListFundsAPIView,

app_name = 'genres'

urlpatterns = [
    path('', CreateGenreAPIView.as_view(), name='root'),  # POST
    path('<int:id>/', GenreByIdAPIView.as_view(), name='by-id'),  # GET, PATCH, DELETE
#    path('list', ListFundsAPIView.as_view(), name='list'),  # GET
]
