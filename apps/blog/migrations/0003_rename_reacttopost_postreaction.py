# Generated by Django 4.0.5 on 2022-08-03 16:50

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0002_remove_post_amount_of_times_read_post_bookmarks_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ReactToPost',
            new_name='PostReaction',
        ),
    ]