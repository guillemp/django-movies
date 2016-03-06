from main.models import Movie, History, Watchlist
movies = Watchlist.objects.all()
movies = Watchlist.objects.values_list('movie', flat=True)

from main.models import Movie, History, Watchlist, Blocklist
from django.utils import timezone