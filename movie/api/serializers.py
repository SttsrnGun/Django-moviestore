from rest_framework import serializers

from movie.models import Movie


class MovieModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Movie
        # fields = '__all__'
        fields = ['id', 'name', 'create_by', 'created', 'is_delete']