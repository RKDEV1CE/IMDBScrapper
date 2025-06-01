from django.urls import path
from .views import MovieListView,filter_movies,get_casts_by_movie
urlpatterns = [
    #path('movies/', MovieListView.as_view(), name='movie-list'),
    path('movies/filter/', filter_movies, name='filter-movies'),
    path('movies/casts/', get_casts_by_movie, name='get_casts_by_movie'),
]