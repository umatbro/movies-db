from rest_framework import serializers

from movies_api import models


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Movie
        fields = '__all__'


class MovieRankingSerializer(serializers.ModelSerializer):
    total_comments = serializers.IntegerField()
    rank = serializers.IntegerField()

    class Meta:
        model = models.Movie
        fields = ('id', 'total_comments', 'rank')
