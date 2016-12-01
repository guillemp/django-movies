from main.models import Movie
from bs4 import BeautifulSoup
import requests

movies = Movie.objects.filter(faff_id__exact='').order_by('-id')
total = len(movies)

i = 1
for movie in movies:
    pos = "%s/%s" % (i, total)
    i += 1
    
    try:
        url = 'http://www.filmaffinity.com/es/search.php?stext={}'.format(movie.title.replace(" ", "+"))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        
        link = soup.findAll("link", { "rel" : "canonical" })
        content = link[0]['href']
        
        if content.startswith('http://www.filmaffinity.com/es/film'):
            faff_id = content.split("/")[4].split(".")[0]
            movie.faff_id = faff_id
            movie.save()
            print pos, movie.id, faff_id
        else:
            print pos, movie.id, "no redirect"
    except Exception, e:
        print movie.id, str(e)