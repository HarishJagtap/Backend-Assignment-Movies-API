from django.contrib import admin

from .models import Movie, Collection

admin.site.register(Movie)
admin.site.register(Collection)