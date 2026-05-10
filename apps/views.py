from django.db.models import Exists, OuterRef, Value, BooleanField, Count, F
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from filters import PostFilter
from models import Post, Like
from permission import IsAuthorOrAdminReadOnly
from serializers import PostModelSerializer, CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class PostModelViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostModelSerializer
    permission_classes = [IsAuthorOrAdminReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PostFilter
    search_fields = ('title', 'content')
    ordering_fields = ('created_at', 'views_count',)
    ordering = ('-created_at',)
    http_method_names = ("get", "post", "patch", "delete")

    def get_queryset(self):
        qs = (super().get_queryset().select_related('category', 'author').prefetch_related('tags'))
        user = self.request.user
        if user.is_authenticated:
            key = Exists(Like.objects.filter(post_id=OuterRef('pk'), user=user))
        else:
            key = Value(False, BooleanField())

        return qs.annotate(
            likes_count=Count("likes"),
            is_liked=key
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views_count = F('views_count') + 1
        instance.save(update_fields=['views_count'])
        instance.refresh_from_db()

        serializer = self.get_serializer(instance=instance)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="like", serializer_class=None)
    def set_like(self, request, pk=None):
        Like.objects.get_or_create(user=request.user, post_id=pk)
        return Response({"status": 'ok'})

    @action(detail=True, methods=["post"], url_path="unlike", serializer_class=None)
    def set_unlike(self, request, pk=None):
        Like.objects.filter(user=request.user, post=pk).delete()
        return Response({"status": 'ok'})

    @action(detail=False, methods=["get"], url_path="my-posts", permission_classes=[IsAuthenticated])
    def my_posts(self, request, pk=None):
        user = self.request.user
        qs = self.get_queryset().filter(author=user)
        response = PostModelSerializer(qs, many=True, context={'request': request}).data
        return Response(response)
