from datetime import datetime

from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.models import Book


class BookModelSerializer(ModelSerializer):
    is_classic = SerializerMethodField()
    available_copies = SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'author','total_copies', 'borrowed_copies', 'published_year', 'rating', 'available_copies', 'is_classic']

    def get_is_classic(self, obj):
        current_year = datetime.now().year
        return (current_year - obj.published_year) >= 10

    def get_available_copies(self, obj):
        return obj.total_copies - obj.borrowed_copies



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        data = cls.token_class.for_user(user)
        data.payload['role'] = user.role
        return data
