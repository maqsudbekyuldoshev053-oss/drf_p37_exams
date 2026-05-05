from datetime import datetime

from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.models import Book


#
#
# class CourseModelSerializer(ModelSerializer):
#     students_count = SerializerMethodField()
#     is_enrolled  = SerializerMethodField()
#     instructor = HiddenField(default=CurrentUserDefault())
#     skills = ListSerializer(child=CharField(max_length=25), write_only=True)
#
#     class Meta:
#         model = Course
#         fields = 'id', 'title', 'description', 'instructor', 'students_count', 'skills', 'is_enrolled'
#
#     def __init__(self, instance=None, data=empty, **kwargs):
#         fields = kwargs['context']['request'].query_params.get('fields')
#         super().__init__(instance, data, **kwargs)
#         if fields:
#             allowed = set(fields.split(','))
#             existing = set(self.fields)
#             for field_name in existing - allowed:
#                 self.fields.pop(field_name)
#
#
#     def get_students_count(self, obj):
#         return getattr(obj, 'student_count', obj.enrollments.count())
#
#
#     def get_is_enrolled(self, obj):
#         request = self.context.get('request')
#
#         if not request or not request.user or not request.user.is_authenticated:
#             return False
#
#         return obj.enrollments.filter(user=request.user).exists()


# def create(self, validated_data):
#     skills = validated_data.pop('skills', [])
#
#     skill_list = []
#     for s in skills:
#         obj, _ = Skill.objects.get_or_create(name=s)
#         skill_list.append(obj)
#
#     instance = Course.objects.create(**validated_data)
#     instance.skill.set(skill_list)
#     return instance
#
# def update(self, instance, validated_data):
#     skills = validated_data.pop('skills', [])
#     skill_list = []
#     for skill in skills:
#         obj, created = Skill.objects.get_or_create(name=skill)
#         skill_list.append(obj)
#     instance.skills.set(skill_list)
#     return super().update(instance, validated_data)


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
