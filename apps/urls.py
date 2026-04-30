from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenRefreshView

from apps.views import (CustomTokenObtainPairView, PostModelViewSet)

router = SimpleRouter(trailing_slash=False)
router.register('posts', PostModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('posts', PostListCreateAPIView.as_view()),
    path('token', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]
