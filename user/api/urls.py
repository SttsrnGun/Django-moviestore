from django.urls import path
from . import views


urlpatterns = [
    path(r'',views.UserListView.as_view()),
    path(r'<int:pk>',views.UserDetailView.as_view()),
]