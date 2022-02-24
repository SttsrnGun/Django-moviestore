from django.contrib import admin
from .models import Movie, MovieList, MovieFavorite


admin.site.register(Movie)
admin.site.register(MovieList)
admin.site.register(MovieFavorite)