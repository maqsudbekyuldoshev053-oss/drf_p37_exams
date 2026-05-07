from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models import CharField, TextChoices

from apps.models.managers import CustomUserManager


class User(AbstractUser):
    class Role(TextChoices):
        Admin = "admin", "Admin"
        Author = "author", "Author"
        Reader = "reader", "Reader"
    role = CharField(max_length=15, choices=Role.choices, default=Role.Reader)
    phone = CharField(max_length=15, unique=True)

    objects = CustomUserManager()