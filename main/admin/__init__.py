from django.contrib import admin
from main import models

class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'imdb_id', 'faff_id')
    search_fields = ('title',)


admin.site.register(models.Movie, MovieAdmin)