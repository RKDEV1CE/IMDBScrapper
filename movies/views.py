from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Movie
from .serializers import MovieSerializer
from rest_framework.decorators import api_view
from django.db.models import Q
from .models import Cast
from .serializers import CastSerializer


class MovieListView(APIView):
    def get(self, request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def filter_movies(request):
    movie_name = request.GET.get('movie_name')
    director = request.GET.get('director')
    release_year = request.GET.get('release_year')
    min_rating = request.GET.get('min_rating')

    filters = Q()
    if movie_name:
        filters &= Q(movie_name__icontains=movie_name)
    if director:
        filters &= Q(director__icontains=director)
    if release_year:
        filters &= Q(release_year=release_year)
    if min_rating:
        filters &= Q(rating__gte=min_rating)

    movies = Movie.objects.filter(filters)
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_casts_by_movie(request):
    movie_id = request.GET.get('movie_id')
    if not movie_id:
        return Response({"error": "movie_id query parameter is required."}, status=400)
    
    casts = Cast.objects.filter(movie_id=movie_id)
    serializer = CastSerializer(casts, many=True)
    return Response(serializer.data)
