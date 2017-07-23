from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Person(models.Model):
    name = models.CharField(max_length=255)
    profile_path = models.CharField(max_length=100)
    
    def url(self):
        return '/person/{}/'.format(self.id)
    
    def image(self):
        if self.profile_path:
            #return 'https://image.tmdb.org/t/p/w185{}'.format(self.profile_path)
            #return 'https://image.tmdb.org/t/p/w132_and_h132_bestv2/{}'.format(self.profile_path)
            return 'https://image.tmdb.org/t/p/w264_and_h264_bestv2/{}'.format(self.profile_path)
        return '/static/img/person.png'
    
    def portrait(self):
        if self.profile_path:
            return 'https://image.tmdb.org/t/p/w300_and_h450_bestv2/{}'.format(self.profile_path)
        return '/static/img/person.png'

class Movie(models.Model):
    title = models.CharField(max_length=255, blank=True)
    original_title = models.CharField(max_length=255, blank=True)
    tagline = models.CharField(max_length=255, blank=True)
    overview = models.TextField(blank=True)
    imdb_id = models.CharField(max_length=20, blank=True)
    imdb_rating = models.FloatField(default=0)
    imdb_votes = models.IntegerField(default=0)
    faff_id = models.CharField(max_length=20, blank=True)
    faff_rating = models.FloatField(default=0)
    faff_votes = models.IntegerField(default=0)
    release_date = models.DateField(null=True, blank=True)
    original_language = models.CharField(max_length=20, blank=True)
    poster_path = models.CharField(max_length=100, blank=True)
    backdrop_path = models.CharField(max_length=100, blank=True)
    runtime = models.CharField(max_length=10, blank=True)
    cast = models.ManyToManyField(Person, through='MovieCast', related_name='movies')
    # control fields
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, related_name='added_movies')
    
    def __unicode__(self):
        return self.title
    
    def url(self):
        return '/movie/{}/'.format(self.id)
    
    def poster(self):
        #return 'https://image.tmdb.org/t/p/w370{}'.format(self.poster_path)
        return 'https://image.tmdb.org/t/p/w600_and_h900_bestv2/{}'.format(self.poster_path)
    
    def poster_small(self):
        #return 'https://image.tmdb.org/t/p/w185_and_h278_bestv2/{}'.format(self.poster_path)
        return 'https://image.tmdb.org/t/p/w370_and_h556_bestv2/{}'.format(self.poster_path)
    
    def backdrop(self):
        #return 'https://image.tmdb.org/t/p/w533_and_h300_bestv2/{}'.format(self.backdrop_path)
        return 'https://image.tmdb.org/t/p/w1066_and_h600_bestv2/{}'.format(self.backdrop_path)
        #return 'https://image.tmdb.org/t/p/w1300_and_h730_bestv2/{}'.format(self.backdrop_path)

class MovieCast(models.Model):
    person = models.ForeignKey(Person)
    movie = models.ForeignKey(Movie)
    order = models.IntegerField(default=0)
    
    class Meta:
        unique_together = (("person", "movie"),)

class History(models.Model):
    user = models.ForeignKey(User, related_name='history')
    movie = models.ForeignKey(Movie)
    rating = models.IntegerField(default=0)
    created = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = (("user", "movie"),)

class Watchlist(models.Model):
    user = models.ForeignKey(User, related_name='watchlist')
    movie = models.ForeignKey(Movie)
    important = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = (("user", "movie"),)

class Blocklist(models.Model):
    user = models.ForeignKey(User, related_name='blocklist')
    movie = models.ForeignKey(Movie)
    created = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = (("user", "movie"),)