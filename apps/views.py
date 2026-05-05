from PIL import Image
from PIL.Image import Image
from django.http import FileResponse, Http404
from django.views import View
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.models import Book
from apps.serializers import CustomTokenObtainPairSerializer, BookModelSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer



@extend_schema(tags=['Book'])
class BookViewSet(ModelViewSet):
    serializer_class = BookModelSerializer

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]

    search_fields = ['title', 'author']
    ordering_fields = ['rating', 'published_year']
    ordering = ['-rating', '-published_year']

    def get_queryset(self):
        return Book.objects.annotate_with_availability()


class BookThumbnailView(View):
    def get(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404

        if not book.image:
            raise Http404

        size = request.GET.get('size', 'small')

        sizes = {
            'small': (100, 100),
            'medium': (300, 300),
            'large': (600, 600),
        }

        image_path = book.image.path

        img = Image.open(image_path)
        img.thumbnail(sizes.get(size, (100, 100)))

        thumb_path = f"{image_path}_{size}.jpg"
        img.save(thumb_path)

        return FileResponse(open(thumb_path, 'rb'), content_type='image/jpeg')