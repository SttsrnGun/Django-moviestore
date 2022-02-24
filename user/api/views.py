from django.contrib.auth.models import User
from rest_framework import generics, permissions

from .serializers import UserModelSerializer


class UserListView(generics.ListAPIView):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserModelSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserModelSerializer
    permission_classes = [permissions.IsAuthenticated]
