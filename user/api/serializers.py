from rest_framework import serializers
from django.contrib.auth.models import User


class UserModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email']