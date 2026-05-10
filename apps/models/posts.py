
from django.db.models import Model, CharField, SlugField, TextField, ForeignKey, CASCADE, ManyToManyField, IntegerField, \
    DateTimeField, BooleanField, PositiveIntegerField


class Category(Model):
    name = CharField(max_length=255, unique=True)
    slug = SlugField(unique=True)

class Tag(Model):
    name = CharField(max_length=255, unique=True)

class Post(Model):
    author = ForeignKey("apps.User", CASCADE, related_name='posts')
    category = ForeignKey("apps.Category", CASCADE, related_name='posts')
    tags = ManyToManyField("apps.Tag", blank=True, related_name='posts')
    title = CharField(max_length=255)
    content = TextField()
    is_published = BooleanField(default=False)
    views_count = PositiveIntegerField(default=0)
    created_at = DateTimeField(auto_now_add=True)

class Like(Model):
    user = ForeignKey("apps.User", CASCADE, related_name='likes')
    post = ForeignKey("apps.Post", CASCADE, related_name='likes')

    class Meta:
        unique_together = (
            ('user', 'post'),
        )
