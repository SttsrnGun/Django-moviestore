from django.urls import path, include
from . import views

app_name = 'authentication'
urlpatterns = [
    path('login/', views.loginView, name='login'),
    path('register/', views.registerView, name='register'),
    path('', include('django.contrib.auth.urls')),
    
    # path('logout', views.postLogout, name='postLogout'),
]
