from __future__ import unicode_literals

from django.db import models


class Hourly(models.Model):
    hourly_base = models.IntegerField()

    def __str__(self):
        return str(self.hourly_base)

