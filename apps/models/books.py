from django.db.models import Model, CharField, IntegerField, ImageField, FloatField, F, Manager


class BookManager(Manager):
    def annotate_with_availability(self):
        return self.get_queryset().annotate(
            available_copies=F('total_copies') - F('borrowed_copies')
        )


class Book(Model):
    title = CharField(max_length=255)
    author = CharField(max_length=255)
    total_copies = IntegerField()
    borrowed_copies = IntegerField(default=0)
    published_year = IntegerField()
    rating = FloatField(default=0)
    image = ImageField(upload_to='books/', null=True, blank=True)
    objects = BookManager()

    def __str__(self):
        return self.title
