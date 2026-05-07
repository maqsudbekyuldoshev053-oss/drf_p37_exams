
from django.db.models import Count, Value, BooleanField, OuterRef, Exists
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.filters import PostFilter
from apps.models import Post
from apps.models.posts import Like
from apps.permission import IsAuthorOrAdminOrReadOnly
from apps.serializers import CustomTokenObtainPairSerializer, PostModelSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@extend_schema(tags=['Post'])
class PostModelViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostModelSerializer
    permission_classes = [IsAuthorOrAdminOrReadOnly]
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = PostFilter
    search_fields = ('title', 'content')
    ordering_fields = ('created_at', 'views_count', 'id')
    http_method_names = ['post', 'get', 'patch']

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user

        if user.is_authenticated:
            key = Exists(Like.objects.filter(post_id=OuterRef('pk'), user=user))
        else:
            key = Value(False, BooleanField())

        return qs.annotate(
            likes_count=Count('likes'),
            is_liked=key
        )

    @action(detail=True, methods=['post'], url_path='like', serializer_class=None)
    def set_like(self, request, pk=None):
        Like.objects.get_or_create(user=request.user, post_id=pk)
        return Response({'status': 'ok'})

    @action(detail=True, methods=['post'], url_path='unlike', serializer_class=None)
    def set_unlike(self, request, pk=None):
        Like.objects.filter(user=request.user, post_id=pk).delete()
        return Response({'status': 'ok'})

    @action(detail=False, methods=['get'], url_path='my-posts', permission_classes=[IsAuthenticated])
    def my_posts(self, request):
        user = self.request.user
        qs = self.get_queryset().filter(author=user)
        response = PostModelSerializer(qs, many=True, context={'request': request}).data
        return Response(response)