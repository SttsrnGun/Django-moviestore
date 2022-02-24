from movie.models import Movie
from rest_framework import generics
from rest_framework.response import Response
from .serializers import MovieModelSerializer


class MovieListView(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieModelSerializer


class MovieDetailView(generics.RetrieveUpdateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieModelSerializer
