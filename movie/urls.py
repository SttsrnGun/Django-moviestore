from django.urls import path, include
from . import views

app_name = 'movies'
urlpatterns = [
    path(r'', views.getList, name='getList'),
    path('<int:id>/', views.getDetail, name='getDetail'),
    
    path(r'<int:movie_id>/favorite/', views.postMovieFavorite, name='postMovieFavorite'),
    path(r'favorite', views.getMovieFavorite, name='getMovieFavorite'),
    
    path(r'<int:movie_id>/list/', views.postMovieList, name='postMovieList'),
    path(r'list/', views.getMovieList, name='getMovieList'),
    
    # path(r'<int:movie_id>/comment/', views.postMovieComment, name='postMovieComment'),
    # path(r'comment/', views.getMovieComment, name='getMovieComment'),
    path(r'fixture/', views.getMovieListFromAPI, name='getMovieListFromAPI'),
    path(r'imagefixture/', views.mockImage, name='mockImage'),

    
]
