# Generated by Django 4.1.7 on 2023-04-23 05:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_video_publiched'),
    ]

    operations = [
        migrations.RenameField(
            model_name='video',
            old_name='publiched',
            new_name='published',
        ),
    ]
