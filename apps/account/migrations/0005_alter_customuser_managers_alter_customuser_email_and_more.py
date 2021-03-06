# Generated by Django 4.0.5 on 2022-07-19 13:57

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_customuser_auth_provider'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='customuser',
            managers=[
            ],
        ),
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(error_messages={'unique': 'A user with this email already exists'}, max_length=100, unique=True, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(help_text='Letters, digits and underscore only.', max_length=30, unique=True, validators=[django.core.validators.RegexValidator(flags=0, message='Enter a valid username. This value may contain only letters, numbers and underscore.', regex='^[\\w]+\\Z'), django.core.validators.MinLengthValidator(5)], verbose_name='username'),
        ),
    ]
