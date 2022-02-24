from functools import reduce
import io

import requests
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from django.template import loader
from django.urls import reverse
from rest_framework.parsers import JSONParser

from .models import Movie, MovieFavorite, MovieList
from .serializers import MovieAPISerializer
import json
import operator
from django.db.models import Q
import os
import urllib
import random
from django.conf import settings

def getList(request):
    movie = Movie.objects.order_by('title').exclude(title__isnull=True).all()
    # movie = Movie.objects.order_by('title').all()

    keywords = request.GET.get('search')
    if keywords:
        movie = Movie.objects.filter(title__icontains=keywords).all()
        
    genres = request.GET.get('genres')
    if genres:
        movie = Movie.objects.filter(genres__icontains=genres).all()
    
    current_page = request.GET.get('page', 1)
    paginator = Paginator(movie, 10)
    page_obj = paginator.get_page(current_page)
    page_range = paginator.get_elided_page_range(number=current_page)
    
    template = loader.get_template('movies/list.html')
    context = {
        'movie': movie,
        'authenticated_user': request.user,
        'is_authenticated': request.user.is_authenticated,
        'page_obj': page_obj,
        'keywords': keywords,
        'genres': genres,
        'page_range': page_range,
    }
    return HttpResponse(template.render(context, request))

def getDetail(request, id):
    user = None
    if(request.user.is_authenticated):
        user = request.user
        
    movie = Movie.objects.filter(pk=id).get()
    movieFavorite = MovieFavorite.objects.filter(user=user, movie=movie)
    movieList = MovieList.objects.filter(user=user, movie=movie)
    template = loader.select_template(['movies/detail.html','base.html','login-section.html'])
    # template = loader.get_template('movies/detail.html')
    print(movie.genres)
    genresList = convertStrToObj(movie.genres)
    # movieListByGenres = getMoviebyType([item['name'] for item in genresList])
    companyList = convertStrToObj(movie.production_companies)

    context = {
        'movie': movie,
        'movieFavorite': movieFavorite,
        'movieList': movieList,
        'authenticated_user': request.user,
        'is_authenticated': request.user.is_authenticated,
        'genresList': genresList,
        # 'movieListByGenres': movieListByGenres[:4],
        'companyList': companyList
    }
    return HttpResponse(template.render(context, request))

def getMovieFavorite(request):
    movie = Movie.objects.filter(pk=id).get()
    movieFavorite = MovieFavorite.objects.filter(user=request.user, movie=movie)
    template = loader.get_template('movies/favorite/list.html')
    context = {
        'movie': movie,
        'movieFavorite': movieFavorite,
    }
    return HttpResponse(template.render(context, request))

@login_required
def postMovieFavorite(request, movie_id):
    try:
        movie = Movie.objects.filter(pk=movie_id).get()
        movieFavorite = MovieFavorite.objects.filter(user=request.user, movie=movie)
        if(movieFavorite.exists()):
            movieFavorite.delete()
        else:
            movieFavorite = MovieFavorite.objects.create(user=request.user , movie=movie)

        return redirect(reverse('movies:getDetail', args=(movie_id,)))
    except (KeyError, Movie.DoesNotExist):
        return redirect(reverse('movies:getList'))

def getMovieList(request):
    movie = Movie.objects.filter(pk=id).get()
    movieList = MovieList.objects.filter(user=request.user, movie=movie)
    template = loader.get_template('movies/list/list.html')
    context = {
        'movie': movie,
        'movieList': movieList,
    }
    return HttpResponse(template.render(context, request))

@login_required
def postMovieList(request, movie_id):
    try:
        movie = Movie.objects.filter(pk=movie_id).get()
        movieList = MovieList.objects.filter(user=request.user, movie=movie)
        if(movieList.exists()):
            movieList.delete()
        else:
            movieList = MovieList.objects.create(user=request.user , movie=movie)

        return redirect(reverse('movies:getDetail', args=(movie_id)))
    except (KeyError, Movie.DoesNotExist):
        return redirect(reverse('movies:getList'))    

def getMovieListFromAPI(request):
    try:
        # payload = {'query_string': 'SELECT id, imdb_id, genres, original_title, title, tagline, overview, popularity, production_companies, release_date, vote_average, vote_count  FROM `fleet-joy-332106.moviestore_workshop.movies_metadata'}
        response = requests.get('https://us-central1-my-project-1552961772347.cloudfunctions.net/function-1')
        if response.status_code != 200:
            return HttpResponseBadRequest('response bad request')
        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        for item in data:
            serialized = MovieAPISerializer(data=data[item])
            print(serialized.is_valid())
            Movie.objects.create(**serialized.data, create_by=request.user)
            
        print('success')
        return HttpResponse("Success!")
    
    except BaseException as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise
        

def mockImage(request):
    try:
        response = requests.get('https://61889f3dd0821900178d73d7.mockapi.io/home-banner')
        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)
        for index, item in enumerate(data):
            print(item['image'], settings.PROJECT_PATH+"/media/movies/"+str(index)+".jpg")
            urllib.request.urlretrieve(item['image'], settings.PROJECT_PATH+"/media/movies/"+str(index)+".jpg")
        movies = Movie.objects.filter(image='').all()
        
        for item in movies:
            item.image = 'movies/'+str(random.choice(range(1,20)))+'.jpg'
            print(item.image)
            item.save()
            
        print('success')
        return HttpResponse("Success!")
    
    except BaseException as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise

# def getMoviebyType(genresList):
    # icontainsquery = reduce(operator.and_, (Q(genres__icontains=x) for x in genresList))
    # movies = Movie.objects.filter(genres__icontains=icontainsquery)
    # return movies

def convertStrToObj(objString):
    print('objString', objString)
    try:
        replacedString = objString.replace("'",'"')
        return json.loads(str(replacedString))
    except BaseException as err:
        print('print from views.movie.convertStrToObj', err)
        return []
