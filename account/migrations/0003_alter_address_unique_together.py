# Generated by Django 5.0.4 on 2024-04-21 19:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_address'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='address',
            unique_together=set(),
        ),
    ]
