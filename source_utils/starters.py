from __future__ import unicode_literals
from django.db import models


class CommonInfo(models.Model):
    slug = models.SlugField(max_length=150, blank=True)
    origin = models.DateTimeField(auto_now_add=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True


class Conflict(CommonInfo):
    conflict_description = models.CharField(
        "Conflict description", 
        max_length=300
    )
    conflict_resolution = models.CharField(
        "Conflict resolution",
        null=True, 
        blank=True, 
        max_length=300
    )

    class Meta:
        abstract = True


class GenericCategory(models.Model):
    """ 
    This model represents a general type of base category offered. 
    """
    slug = models.SlugField(max_length=100, blank=True)
    category = models.CharField(
        max_length=30, 
        unique=True
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.category
