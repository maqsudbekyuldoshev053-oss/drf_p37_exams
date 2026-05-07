from django.db.models import Model, TextField, CharField, ForeignKey, CASCADE, BooleanField, ManyToManyField, \
    PositiveIntegerField, SlugField
from django.db.models.fields import DateTimeField
from django.utils.text import slugify


class Category(Model):
    name = CharField(max_length=150, unique=True)
    slug =SlugField(max_length=150)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save()

    def __str__(self):
        return self.name



class Tag(Model):
    name = CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name



class Post(Model):
    title = CharField(max_length=200)
    content = TextField()
    author = ForeignKey('apps.User', CASCADE, related_name="posts")
    category = ForeignKey('apps.Category', CASCADE, related_name="posts")
    tags = ManyToManyField('apps.Tag', blank=True, related_name="posts")
    is_published = BooleanField(db_default=False)
    views_count = PositiveIntegerField(db_default=0)
    created_at = DateTimeField(auto_now=True)



    def __str__(self):
        return self.title


class Like(Model):
    user = ForeignKey('apps.User', CASCADE, related_name="likes")
    post = ForeignKey('apps.Post', CASCADE, related_name="likes")

    class Meta:
        unique_together = (
            ('user', 'post'),
        )