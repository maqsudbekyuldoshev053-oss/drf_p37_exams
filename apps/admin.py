from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from apps.models import Category, Post
from apps.models.users import User
from models import Like


@admin.register(User)
class UserModelView(UserAdmin):
    add_fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", "role" )}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )



class LikeInline(admin.TabularInline):
    model = Like
    extra = 1 
    readonly_fields = ('user',)



@admin.register(Post)
class PostModelView(ModelAdmin):
    list_display = ('title', 'content', 'category', 'views_count', 'is_published')
    readonly_fields = ('views_count',)
    inlines = [LikeInline]
    search_fields = 'title',
    list_filter = 'is_published',