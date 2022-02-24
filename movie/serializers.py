from rest_framework import serializers

from movie.models import Movie


class MovieModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'
        # fields = ['id', 'name', 'create_by', 'created', 'is_delete']
        
class MovieAPISerializer(serializers.Serializer):
    id = serializers.IntegerField( allow_null=True)
    imdb_id = serializers.CharField(allow_null=True)
    genres = serializers.CharField(allow_null=True)
    original_title = serializers.CharField(allow_null=True)
    title = serializers.CharField(allow_null=True)
    tagline = serializers.CharField(allow_null=True)
    overview = serializers.CharField(allow_null=True)
    popularity = serializers.FloatField(allow_null=True)
    production_companies = serializers.CharField(allow_null=True)
    # DATE_INPUT_FORMATS = ['MM/DD/YYYY']
    # release_date = serializers.DateField(allow_null=True, input_formats=DATE_INPUT_FORMATS)
    # release_date = serializers.CharField(allow_null=True)
    vote_average = serializers.FloatField(allow_null=True)
    vote_count = serializers.FloatField(allow_null=True)
    class Meta:
        model = Movie
        # fields = ['id','name', 'imdb_id', 'genres', 'original_title', 'title', 'tagline', 'overview', 'popularity', 'production_companies', 'release_date', 'vote_average', 'vote_count']
        fields = '__all__'

    def create(self, validated_data):
        return Movie.objects.create(**validated_data)
