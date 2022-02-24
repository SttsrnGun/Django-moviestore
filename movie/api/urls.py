from django.urls import path

from . import views

app_name = 'api.movies'
urlpatterns = [
    path(r'', views.MovieListView.as_view()),
    path(r'<int:pk>', views.MovieDetailView.as_view()),
]
