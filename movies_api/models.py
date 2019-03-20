from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=120, blank=False, unique=True)
    cover = models.URLField(null=True)
    release_date = models.DateField(null=True)
    duration = models.IntegerField(null=True)  # movie duration in minutes
    director = models.CharField(max_length=100, null=True)
    website = models.URLField(null=True)

    def __repr__(self):
        return f'Movie(id={self.pk}, title=\'{self.title}\')'

    def __str__(self):
        return repr(self)
