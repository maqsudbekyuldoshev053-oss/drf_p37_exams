from django_filters import NumberFilter, DateTimeFilter
from django_filters.rest_framework import FilterSet

from apps.models import Post


class PostFilter(FilterSet):
    from_time = DateTimeFilter(field_name='created_at', lookup_expr='gte')
    to_time = DateTimeFilter(field_name='created_at', lookup_expr='lte')
    view_count = NumberFilter(field_name='views_count', lookup_expr='gt')

    class Meta:
        model = Post
        fields = ('category', 'tags')