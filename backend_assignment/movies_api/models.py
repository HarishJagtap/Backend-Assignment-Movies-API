from django.db import models
from django.contrib.auth.models import User
import uuid


class Movie(models.Model):
    title = models.TextField()
    description = models.TextField(blank=True)
    genres = models.TextField(blank=True)
    uuid = models.UUIDField(primary_key=True, editable=True)


class Collection(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    movies = models.ManyToManyField(Movie)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
