import django_filters
from movies_api.models import Movie


class MovieFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    duration__gt = django_filters.NumberFilter(field_name='duration', lookup_expr='gt')
    duration__lt = django_filters.NumberFilter(field_name='duration', lookup_expr='lt')

    release_year = django_filters.NumberFilter(field_name='release_date', lookup_expr='year')
    release_year__gt = django_filters.NumberFilter(field_name='release_date', lookup_expr='year__gt')
    release_year__lt = django_filters.NumberFilter(field_name='release_date', lookup_expr='year__lt')
    director = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Movie
        fields = ('release_date', )
