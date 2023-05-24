import datetime
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from users.vk_open import delete_object


# Create your models here.

class User(AbstractUser):
    email = models.EmailField(max_length=254, verbose_name='Email', unique=True)
    name = models.CharField(max_length=30, verbose_name='Публичное имя', default="default name")
    birthday = models.DateField(null=True, verbose_name='Дата рождения')
    avatar = models.CharField(max_length=400, verbose_name='Аватар', default='users/avatars/default_avatar.jpg')

    def __str__(self):
        return self.username

    def get_absolute_url_avatar(self):
        return f"https://ik.imagekit.io/VideoHosting/{self.avatar}"

    def save(self, *args, **kwargs):
        try:
            old_avatar = User.objects.get(pk=self.pk).avatar
            if self.avatar != old_avatar and old_avatar != "users/avatars/default_avatar.jpg":
                delete_object(old_avatar)
        except User.DoesNotExist:
            pass

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.avatar != "users/avatars/default_avatar.jpg":
            delete_object(self.avatar)
        super(User, self).delete(*args, **kwargs)


class Video(models.Model):
    id_video = models.UUIDField(primary_key=True, default=uuid.uuid4, verbose_name='ID')
    username = models.ForeignKey('User', on_delete=models.CASCADE, null=False)
    file = models.CharField(max_length=400, verbose_name='Файл')
    title = models.CharField(max_length=100, verbose_name='Название', default="Default title")
    description = models.TextField(max_length=3000, verbose_name='Описание', default="Default description", blank=True)
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    preview = models.CharField(max_length=400, verbose_name='Превью', default="users/avatars/default_avatar.jpg")
    published = models.BooleanField(default=False, verbose_name='Опубликовано')

    def get_absolute_preview_url(self):
        return f"https://ik.imagekit.io/VideoHosting/{self.preview}"

    def get_absolute_video_url(self):
        return f"https://ik.imagekit.io/VideoHosting/{self.file}"

    def __str__(self):
        return f"[{self.username}] {self.title}"

    class Meta:
        ordering = ['-date']
        verbose_name = "Видео"
        verbose_name_plural = verbose_name

    def delete(self, *args, **kwargs):
        delete_object(self.file)
        if self.preview != "users/avatars/default_avatar.jpg":
            delete_object(self.preview)
        super(Video, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        try:
            old = Video.objects.get(pk=self.pk)
            if not old.published and self.published:
                self.date = datetime.datetime.now()
            old_preview = old.preview
            if self.preview != old_preview and old_preview != "users/avatars/default_avatar.jpg":
                delete_object(old_preview)
        except Video.DoesNotExist:
            pass

        super().save(*args, **kwargs)


class Likes(models.Model):
    username = models.ForeignKey('User', on_delete=models.CASCADE, null=False)
    video = models.ForeignKey('Video', on_delete=models.CASCADE, null=False)

    class Meta:
        unique_together = ('username', 'video')
        verbose_name = "Лайк"
        verbose_name_plural = "Лайки"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if Dislikes.objects.filter(username=self.username, video=self.video).exists():
            dislike = Dislikes.objects.get(username=self.username, video=self.video)
            dislike.delete()
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    def __str__(self):
        return self.username.username + " --> " + f"[{self.video.username}] {self.video.title}"


class Dislikes(models.Model):
    username = models.ForeignKey('User', on_delete=models.CASCADE, null=False)
    video = models.ForeignKey('Video', on_delete=models.CASCADE, null=False)

    class Meta:
        unique_together = ('username', 'video')
        verbose_name = "Дизлайк"
        verbose_name_plural = "Дизлайки"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if Likes.objects.filter(username=self.username, video=self.video).exists():
            like = Likes.objects.get(username=self.username, video=self.video)
            like.delete()
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    def __str__(self):
        return self.username.username + " --> " + f"[{self.video.username}] {self.video.title}"


class History(models.Model):
    username = models.ForeignKey('User', on_delete=models.CASCADE, null=False)
    video = models.ForeignKey('Video', on_delete=models.CASCADE, null=False)
    progress = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        verbose_name = "История"
        verbose_name_plural = "История"
        unique_together = ('username', 'video')

    def __str__(self):
        return self.username.username + " --> " + self.video.title + ". Date: " + self.date.strftime("%d/%m/%Y %H:%M:%S")


class Comments(models.Model):
    username = models.ForeignKey('User', on_delete=models.CASCADE, null=False)
    video = models.ForeignKey('Video', on_delete=models.CASCADE, null=False)
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    text = models.TextField(max_length=1000, verbose_name='Содержание')

    class Meta:
        ordering = ['-date']
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def delete_comment(self, user):
        if user == self.username:
            self.delete()
