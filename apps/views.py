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


#
# @extend_schema(tags=['Course'])
# class CourseModelViewSet(ModelViewSet):
#     queryset = Course.objects.all()
#     serializer_class = CourseModelSerializer
#     permission_classes = [IsAdminAuthorOrReadOnly]
#     filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
#     search_fields = ('title', 'description')
#     ordering_fields = ('id',)
#     http_method_names = ['post', 'get', 'patch']
#     pagination_class = None
#
#     def get_queryset(self):
#         qs = super().get_queryset()
#         user = self.request.user
#
#         if user.is_authenticated:
#             key = Exists(Enrollment.objects.filter(course=OuterRef('pk'), user=user))
#         else:
#             key = Value(False, BooleanField())
#
#         return qs.annotate(
#             students_count=Count('enrollments'),
#             is_enrolled=key
#         )
#
#     @action(detail=True, methods=['post'], url_path='enrollment', serializer_class=None)
#     def set_like(self, request, pk=None):
#         Enrollment.objects.get_or_create(user=request.user, course_id=pk)
#         return Response({'status': 'ok'})
#
#     @action(detail=True, methods=['post'], url_path='unenrollment', serializer_class=None)
#     def set_unlike(self, request, pk=None):
#         Enrollment.objects.filter(user=request.user, course_id=pk).delete()
#         return Response({'status': 'ok'})

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