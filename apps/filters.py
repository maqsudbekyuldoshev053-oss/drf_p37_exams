from django_filters import NumberFilter, DateTimeFilter, CharFilter
from django_filters.rest_framework import FilterSet

from apps.models import Post


class PostFilter(FilterSet):
    category = NumberFilter(field_name='category_id')
    tags = CharFilter(field_name='tags__name', lookup_expr='icontains')

    class Meta:
        model = Post
        fields = ('category', 'tags')
