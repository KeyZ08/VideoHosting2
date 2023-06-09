# Generated by Django 4.1.7 on 2023-04-22 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_video_description_alter_video_preview_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='description',
            field=models.TextField(default='', max_length=2000, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='video',
            name='preview',
            field=models.CharField(default='users/avatars/default_avatar.jpg', max_length=400, verbose_name='Превью'),
        ),
        migrations.AlterField(
            model_name='video',
            name='title',
            field=models.CharField(default='', max_length=100, verbose_name='Название'),
        ),
    ]
