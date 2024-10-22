# Generated by Django 5.0.6 on 2024-07-11 19:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_alter_customuser_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='password',
            field=models.CharField(max_length=255, validators=[django.core.validators.RegexValidator(message='Password must contain at least 8 characters, including uppercase, lowercase, and digits.', regex='^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)[a-zA-Z\\d]{8,}$|^pbkdf2_sha256\\$[0-9]+\\$.+$')]),
        ),
    ]
