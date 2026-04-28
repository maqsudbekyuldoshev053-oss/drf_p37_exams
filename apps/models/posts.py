from django.db.models import Model, TextField, CharField, ForeignKey, CASCADE, BooleanField, ManyToManyField, \
    PositiveIntegerField
from django.db.models.fields import DateTimeField


class Category(Model):
    name = CharField(max_length=150)

class Tag(Model):
    name = CharField(max_length=150)

class Post(Model):
    title = CharField(max_length=200)
    content = TextField()
    is_published = BooleanField(db_default=False)
    author = ForeignKey('apps.User', CASCADE, related_name="posts")
    category = ForeignKey('apps.Category', CASCADE, related_name="posts")
    tags = ManyToManyField('apps.Tag', blank=True,  related_name="posts")
    views_count = PositiveIntegerField(db_default=0)
    created_at = DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Like(Model):
    user = ForeignKey('apps.User', CASCADE, related_name="likes")
    posts = ForeignKey('apps.Post', CASCADE, related_name="likes")

    class Meta:
        unique_together = (
            ('user', 'posts')
        )