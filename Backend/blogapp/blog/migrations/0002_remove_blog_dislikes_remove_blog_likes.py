# Generated by Django 4.2.3 on 2023-08-01 07:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='dislikes',
        ),
        migrations.RemoveField(
            model_name='blog',
            name='likes',
        ),
    ]
