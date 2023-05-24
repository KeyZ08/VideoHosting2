import django.contrib.auth.admin
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.utils.html import format_html

from users.models import *

# Register your models here.
User = get_user_model()
admin.site.register(Likes)
admin.site.register(Dislikes)


@admin.register(User)
class UserAdmin(UserAdmin):
    readonly_fields = ['avatar_image']
    list_display = ['username', 'name', 'email', 'is_staff', "avatar_image"]
    fieldsets = (
        (None, {"fields": ("username", "password", "email", "name", "birthday")}),
        (('Avatar'), {'fields': ('avatar', 'avatar_image')}),
        (("Important dates"), {"fields": ("last_login", "date_joined")}),
        (
            ("Permissions"),
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
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "email", "name", "birthday"),
            },
        ),
    )

    def avatar_image(self, obj):
        return format_html('<img src="{}" width="100"/>'.format(obj.get_absolute_url_avatar()))

    def delete_queryset(self, request, queryset):
        for i in queryset:
            i.delete()

    avatar_image.short_description = 'Avatar'


@admin.register(Video)
class UserVideo(ModelAdmin):
    readonly_fields = ['id_video', 'username', 'date', "views_count", "likes_count", "dislikes_count", "preview_image", "preview", "file"]
    list_display = ['id_video', 'username', 'title', 'date', "preview_image", "published"]

    def preview_image(self, obj):
        return format_html('<img src="{}" width="100"/>'.format(obj.get_absolute_preview_url()))

    def views_count(self, obj):
        return obj.history_set.count()

    def likes_count(self, obj):
        return obj.likes_set.count()

    def dislikes_count(self, obj):
        return obj.dislikes_set.count()

    def delete_queryset(self, request, queryset):
        for i in queryset:
            i.delete()

    preview_image.short_description = 'Preview'
    views_count.short_description = 'Количество просмотров'


@admin.register(Comments)
class UserComments(ModelAdmin):
    readonly_fields = ['video', 'username']
    list_display = ['video', 'username', 'text', 'date']


@admin.register(History)
class UserHistory(ModelAdmin):
    list_display = ['video', 'username', 'progress', 'date']
