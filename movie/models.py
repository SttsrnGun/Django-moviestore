from django.contrib.auth.models import User
from django.db import models


class Movie(models.Model):
    # name = models.CharField(max_length=100, blank=True, default='')
    create_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=False)
    movie_id = models.CharField(blank=True, max_length=100, null=True)
    imdb_id = models.CharField(blank=True, max_length=100, null=True)
    genres = models.TextField(blank=True, null=True)
    original_title = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True, default='title is unavailable')
    tagline = models.TextField(blank=True, null=True)
    overview = models.TextField(blank=True, null=True)
    popularity = models.FloatField(blank=True, null=True)
    production_companies = models.TextField(blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    vote_average = models.FloatField(blank=True, null=True)
    vote_count = models.IntegerField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='movies', default='img/no-image.jpg')
    class Meta:
        ordering = ['created']

    def __str__(self):
        return str(self.title)

    def delete(self):
        self.is_delete = True
        return self.save()
    
    def create(self, validated_data):
        return Movie.objects.create(**validated_data)


class MovieList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return str(self.id)

class MovieFavorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return str(self.id)
