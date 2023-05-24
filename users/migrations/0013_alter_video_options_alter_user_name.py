# Generated by Django 4.1.7 on 2023-05-13 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_alter_comments_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='video',
            options={'ordering': ['-date'], 'verbose_name': 'Видео', 'verbose_name_plural': 'Видео'},
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(default='default name', max_length=30, verbose_name='Публичное имя'),
        ),
    ]