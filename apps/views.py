from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.filters import PostFilter
from apps.models import Post
from apps.models.posts import Like
from apps.permission import IsAuthorReadOrWrite
from apps.serializers import PostListSerializerModel, CustomTokenObtainPairSerializer, PostSerializerModel


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


#
@extend_schema(tags=['Post'])


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class PostModelViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializerModel
    http_method_names = ['get', 'post']

    @action(detail=True, methods=['post'], url_path='like', serializer_class=None)
    def set_like(self, request, pk=None):
        Like.objects.get_or_create(user=request.user, post_id=pk)
        return Response({'status': 'ok'})

    @action(detail=True, methods=['post'], url_path='unlike', serializer_class=None)
    def set_unlike(self, request, pk=None):
        Like.objects.filter(user=request.user, post_id=pk).delete()
        return Response({'status': 'ok'})



# @extend_schema(tags=['Post'])
# class PostListCreateAPIView(ListCreateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializerModel
#     permission_classes = [IsAuthorReadOrWrite]
#     filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
#     filterset_class = PostFilter
#     search_fields = ('title', 'content')
#     ordering_fields = ('created_at', 'views_count', 'likes_count')

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.annotate(likes_count=Count('likes'))


"""
"refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3NzQ1ODQ3NSwiaWF0IjoxNzc3MzcyMDc1LCJqdGkiOiJjZWQzMmNjNzk3ZTU0YzI0YjQ4NWQyNTEyMjZjMWI1MiIsInVzZXJfaWQiOiIxIiwicm9sZSI6ImFkbWluIn0.Nkb6rxkEOTAoBitoGNAhctvMYcvxC6wRcM9SEri7d50",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzc3Mzc1Njc1LCJpYXQiOjE3NzczNzIwNzUsImp0aSI6ImRiNTNmMDkwNDFjYjQ0ZWI5M2RhNWYzZjU0NmVlOGE0IiwidXNlcl9pZCI6IjEiLCJyb2xlIjoiYWRtaW4ifQ.n-4OUQQ67b6kO1mXnj_FcyUlR9H52Bhy2yJYkDxKGAc"
  """
