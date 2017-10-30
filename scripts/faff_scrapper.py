from datetime import datetime
from django.utils import timezone
from main.models import Movie
from bs4 import BeautifulSoup
import requests

movies = Movie.objects.exclude(faff_id__exact='').order_by('faff_date')
total = len(movies)

i = 1
for movie in movies:
    pos = "%s/%s" % (i, total)
    i += 1
    
    try:
        url = 'http://www.filmaffinity.com/es/{}.html'.format(movie.faff_id)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        
        div = soup.findAll("div", { "itemprop" : "ratingValue" })
        rating = float(div[0]['content'])
        
        span = soup.findAll("span", { "itemprop" : "ratingCount" })
        votes = int(span[0]['content'])
        
        changes = False
    
        rating_out = ""
        if rating != movie.faff_rating:
            rating_out = "%s => %s" % (movie.faff_rating, rating)
            movie.faff_rating = rating
            changes = True
        
        votes_out = ""
        if votes != movie.faff_votes:
            votes_out = "%s => %s (+%s)" % (movie.faff_votes, votes, (votes-movie.faff_votes))
            movie.faff_votes = votes
            changes = True
        
        movie.faff_date = timezone.now()
        movie.save()
        
        print pos, movie.faff_id, rating_out, votes_out, movie.title.encode('utf-8')
    except Exception, e:
        print movie.faff_id, str(e)

