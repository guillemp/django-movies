from main import models

#movies
movies = models.Movie.objects.all()
for movie in movies:
    models.Activity.add(movie.user, movie, 'movie_add', created=movie.created)


#history
history = models.History.objects.all()
for h in history:
    models.Activity.add(h.user, h.movie, 'history_add', created=h.created)

#whatchlist
whatchlist = models.Watchlist.objects.all()
for w in whatchlist:
    models.Activity.add(w.user, w.movie, 'history_add', created=w.created)
