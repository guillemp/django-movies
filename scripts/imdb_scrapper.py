from main.models import Movie
from bs4 import BeautifulSoup
import requests

movies = Movie.objects.all().order_by('-id')
total = len(movies)

i = 1
for movie in movies:
    pos = "%s/%s" % (i, total)
    i += 1
    
    try:
        url = 'http://www.imdb.com/title/{}/'.format(movie.imdb_id)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
    
        span = soup.findAll("span", { "itemprop" : "ratingValue" })
        rating = float(span[0].contents[0])
    
        span = soup.findAll("span", { "itemprop" : "ratingCount" })
        votes = span[0].contents[0]
        votes = int(votes.replace(",", ""))
    
        changes = False
    
        rating_out = ""
        if rating != movie.imdb_rating:
            rating_out = "%s => %s" % (movie.imdb_rating, rating)
            movie.imdb_rating = rating
            changes = True
    
        votes_out = ""
        if votes != movie.imdb_votes:
            votes_out = "%s => %s" % (movie.imdb_votes, votes)
            movie.imdb_votes = votes
            changes = True
    
        if changes:
            movie.save()
    
        print pos, movie.imdb_id, rating_out, votes_out
    except Exception, e:
        print movie.imdb_id, str(e)

