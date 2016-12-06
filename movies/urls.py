from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import TemplateView, RedirectView
from main import views
from main.views import api, auth, add, ajax

urlpatterns = [
    url(r'^$', views.index_view, name='index_view'),
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^discover/$', views.discover_view, name='discover_view'),
    url(r'^latest/$', views.latest_view, name='latest_view'),
    url(r'^users/$', views.users_view, name='users_view'),
    url(r'^search/$', views.search_view, name='search_view'),
    url(r'^add/$', add.movie_add, name='movie_add'),
    url(r'^top/imdb/$', views.top_imdb_view, name='top_imdb_view'),
    url(r'^top/filmaffinity/$', views.top_fa_view, name='top_fa_view'),
    url(r'^top/$', RedirectView.as_view(pattern_name='top_imdb_view', permanent=False)),
    
    # statics
    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/img/favicon.ico')),
    
    # auth
    url(r'^login/$', auth.login_view, name='login_view'),
    url(r'^logout/$', auth.logout_view, name='logout_view'),
    url(r'^settings/$', auth.settings_view, name='settings_view'),
    
    # movie
    url(r'^movie/(?P<movie_id>[0-9]+)/$', views.movie_view, name='movie_view'),
    
    # person
    url(r'^person/(?P<person_id>[0-9]+)/$', views.person_view, name='person_view'),
    
    # ajax
    url(r'^ajax/history_add_remove/$', ajax.history_add_remove, name='history_add_remove'),
    url(r'^ajax/watchlist_add_remove/$', ajax.watchlist_add_remove, name='watchlist_add_remove'),
    url(r'^ajax/blocklist_add_remove/$', ajax.blocklist_add_remove, name='blocklist_add_remove'),
    url(r'^ajax/watchlist_important/$', ajax.watchlist_important, name='watchlist_important'),
    url(r'^ajax/autocomplete/$', ajax.autocomplete_view, name='autocomplete_view'),
    url(r'^ajax/rating_mode/$', ajax.rating_mode, name='rating_mode'),
    url(r'^ajax/movie_save/$', add.movie_save, name='movie_save'),
    url(r'^ajax/movie_update/$', add.movie_update, name='movie_update'),
    
    # api
    url(r'^api/v1/top/$', api.movies_top, name='api_top_movies'),
    url(r'^api/v1/latest/$', api.latest_view, name='api_latest_movies'),
    url(r'^api/v1/movies/(?P<movie_id>[0-9]+)/$', api.movies_detail, name='api_movies_detail'),
    url(r'^api/v1/movies/$', api.movies_view, name='api_movies_view'),
    url(r'^api/v1/(?P<username>[a-zA-Z0-9_]+)/history/$', api.history_view, name='api_history_view'),
    url(r'^api/v1/(?P<username>[a-zA-Z0-9_]+)/watchlist/$', api.watchlist_view, name='api_watchlist_view'),
    url(r'^api/v1/(?P<username>[a-zA-Z0-9_]+)/blocklist/$', api.blocklist_view, name='api_blocklist_view'),
    
    # user
    url(r'^(?P<username>[a-zA-Z0-9_]+)/history/$', views.history_view, name='history_view'),
    url(r'^(?P<username>[a-zA-Z0-9_]+)/watchlist/$', views.watchlist_view, name='watchlist_view'),
    url(r'^(?P<username>[a-zA-Z0-9_]+)/blocklist/$', views.blocklist_view, name='blocklist_view'),
    url(r'^(?P<username>[a-zA-Z0-9_]+)/added/$', views.added_view, name='added_view'),
    url(r'^(?P<username>[a-zA-Z0-9_]+)/$', views.profile_view, name='profile_view'),
]
