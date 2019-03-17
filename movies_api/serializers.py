from rest_framework import serializers

from movies_api import models


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Movie
        fields = '__all__'
