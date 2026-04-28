from rest_framework.fields import HiddenField, CurrentUserDefault, DateTimeField, SerializerMethodField
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.models import Post

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        data = cls.token_class.for_user(user)
        data.payload['role'] = user.role
        return data



class PostSerializerModel(ModelSerializer):
    likes_count = SerializerMethodField()
    # author = HiddenField(default=CurrentUserDefault())
    # created_at = DateTimeField(format='%d-%m-%Y %H:%M', read_only=True)

    class Meta:
        model = Post
        fields = 'id', 'title', 'content', 'is_published', 'author',  'category', 'tags', 'views_count', 'likes_count', 'created_at'
        read_only_fields = ('views_count',)

    def get_likes_count(self, obj: Post):
        return obj.likes_count