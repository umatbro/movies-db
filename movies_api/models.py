from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=120, blank=False)
    cover = models.URLField()
    release_date = models.DateField(blank=True)
    duration = models.IntegerField()  # movie duration in minutes
    director = models.CharField(max_length=100, blank=True)
    website = models.URLField()
