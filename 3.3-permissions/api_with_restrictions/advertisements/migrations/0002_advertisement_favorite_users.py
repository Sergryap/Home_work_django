# Generated by Django 4.0.6 on 2022-08-30 08:57

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('advertisements', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisement',
            name='favorite_users',
            field=models.ManyToManyField(blank=True, null=True, related_name='favorite_advertisements', to=settings.AUTH_USER_MODEL),
        ),
    ]
