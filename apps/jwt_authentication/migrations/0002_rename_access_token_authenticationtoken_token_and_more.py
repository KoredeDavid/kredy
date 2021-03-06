# Generated by Django 4.0.5 on 2022-07-18 15:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('jwt_authentication', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='authenticationtoken',
            old_name='access_token',
            new_name='token',
        ),
        migrations.RemoveField(
            model_name='authenticationtoken',
            name='refresh_token',
        ),
        migrations.AddField(
            model_name='authenticationtoken',
            name='blacklist',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='authenticationtoken',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_token', to=settings.AUTH_USER_MODEL),
        ),
    ]
