from main.models import Movie
from bs4 import BeautifulSoup
import requests
import urllib
import re

movies = Movie.objects.filter(faff_id__exact='').order_by('-id')
total = len(movies)

i = 1
for movie in movies:
    pos = "%s/%s" % (i, total)
    i += 1
    
    params = {
        'stext': movie.title.encode('utf-8'),
        'fromyear': movie.release_date.year,
        'toyear': movie.release_date.year
    }
    url = 'http://www.filmaffinity.com/es/advsearch.php?{}'.format(urllib.urlencode(params))
    
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        
        items = soup.findAll("div", { "class" : "adv-search-item" })
        if len(items) == 1:
            div = soup.findAll("div", { "class" : "mc-title" })
            faff_id = div[0].find_all("a", href=True)[0]['href'].split("/")[2].split(".")[0]
            movie.faff_id = faff_id
            movie.save()
            print movie.title.encode('utf-8'), div[0].contents[0], faff_id
        else:
            print 'SKIPPED'
    
    except Exception, e:
        print movie.id, str(e)