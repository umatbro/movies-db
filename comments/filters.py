import django_filters
from comments.models import Comment


class CommentFilter(django_filters.FilterSet):
    class Meta:
        model = Comment
        fields = ('movie_id',)
