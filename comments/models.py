from django.db import models
import datetime
from movies_api import models as movie_models


class Comment(models.Model):
    movie = models.ForeignKey(movie_models.Movie, null=False, on_delete=models.CASCADE)
    body = models.TextField(blank=True)
    publish_date = models.DateField(default=datetime.date.today)
