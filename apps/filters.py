from django_filters import NumberFilter, DateTimeFilter
from django_filters.rest_framework import FilterSet

from apps.models import Post


class PostFilter(FilterSet):
    view_count = NumberFilter(field_name='views_count', lookup_expr='gt')

    class Meta:
        model = Post
        fields = ('category', 'tags')