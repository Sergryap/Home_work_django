from django.db import models


class Phone(models.Model):
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    release_date = models.DateField()
    lte_exists = models.BooleanField(default=True)
    slug = models.SlugField(max_length=100, allow_unicode=True)
