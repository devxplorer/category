from django.db import models


class User(models.Model):
    username = models.CharField(max_length=30)


class Outfit(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    content = models.CharField(max_length=30)


class Category(models.Model):
    owner = models.ForeignKey(User, null=True, blank=True)
    name = models.CharField(max_length=20)
    outfits = models.ManyToManyField(Outfit, related_name="categories", blank=True)
