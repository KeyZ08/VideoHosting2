# Generated by Django 4.1.7 on 2023-05-08 12:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_alter_history_options_alter_history_unique_together'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comments',
            options={'ordering': ['-date'], 'verbose_name': 'Комментарий', 'verbose_name_plural': 'Комментарии'},
        ),
    ]
