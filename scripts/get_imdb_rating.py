from django.utils import timezone
from main.models import Movie
import requests
import json

movies = Movie.objects.all().order_by('-id')
total = len(movies)

i = 1
for movie in movies:
    pos = "%s/%s" % (i, total)
    i += 1
    url = 'http://www.omdbapi.com/?i=%s&plot=short&r=json' % movie.imdb_id
    try:
        response = requests.get(url)
        data = json.loads(response.text)
        if data.get('imdbRating', False):
            if data['imdbRating'] != "N/A" and data['imdbVotes'] != "N/A":
                r = ""
                v = ""
                changes = False
                rating = data['imdbRating']
                votes = data['imdbVotes'].replace(",", "")

                if float(rating) != float(movie.imdb_rating):
                    r = "%s => %s" % (movie.imdb_rating, rating)
                    movie.imdb_rating = rating
                    changes = True

                if int(votes) != int(movie.imdb_votes):
                    v = "%s => %s" % (movie.imdb_votes, votes)
                    movie.imdb_votes = votes
                    changes = True
                
                movie.save()

                if changes:
                    print pos, movie.imdb_id, r, v
                else:
                    print pos, movie.imdb_id, "..."
            else:
                print pos, movie.imdb_id, "N/A"
        else:
            print pos, movie.imdb_id, "NOx"
    except:
        print pos, movie.imdb_id, "www"
