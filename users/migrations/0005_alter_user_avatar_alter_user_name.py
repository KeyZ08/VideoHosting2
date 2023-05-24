# Generated by Django 4.1.7 on 2023-04-21 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_remove_videoimage_video_user_avatar_video_preview_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.CharField(default='users/avatars/default_avatar.jpg', max_length=400, verbose_name='Аватар'),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=30, verbose_name='Публичное имя'),
        ),
    ]
