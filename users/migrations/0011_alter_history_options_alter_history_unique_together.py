# Generated by Django 4.1.7 on 2023-05-07 07:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_dislikes_options_alter_history_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='history',
            options={'ordering': ['-date'], 'verbose_name': 'История', 'verbose_name_plural': 'История'},
        ),
        migrations.AlterUniqueTogether(
            name='history',
            unique_together={('username', 'video')},
        ),
    ]
