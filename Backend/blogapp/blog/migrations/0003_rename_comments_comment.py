# Generated by Django 4.1.2 on 2023-07-24 16:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_blog_bloguser_likedisklike_comments_blog_user'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Comments',
            new_name='Comment',
        ),
    ]