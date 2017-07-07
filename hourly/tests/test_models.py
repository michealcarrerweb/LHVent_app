from __future__ import unicode_literals

from django.test import TestCase

from hourly.models import Hourly


class HourlyTest(TestCase):

    def create_hourly(self):
        return Hourly.objects.create(hourly_base=10)

    def test_hourly_creation(self):
        w = self.create_hourly()
        self.assertTrue(isinstance(w, Hourly))
        self.assertEqual(w.__str__(), str(w.hourly_base))
