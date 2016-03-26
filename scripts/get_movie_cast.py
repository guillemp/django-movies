from django.utils import timezone
from main.models import Movie, Person, MovieCast
from movies import config
import tmdbsimple as tmdb
import requests
import json

tmdb.API_KEY = config.TMDB_KEY

movies = Movie.objects.all()

for movie in movies:
    if movie.cast.all().count() > 0:
        #print movie.id, "SKIPPED"
        continue
    else:
        print movie.id
    
    request = tmdb.Movies(movie.id)
    response = request.credits()
    
    for p in response['cast']:
        try:
            person = Person()
            person.id = p['id']
            person.name = p['name'] or ''
            person.profile_path = p['profile_path'] or ''
            person.save()
        except Exception, e:
            print str(e)
        
        order = p['order'] or 0
        
        try:
            movie_cast = MovieCast(person=person, movie=movie, order=order)
            movie_cast.save()
        except Exception, e:
            print str(e)