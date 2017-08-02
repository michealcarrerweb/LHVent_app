from __future__ import unicode_literals

import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from stock.models import Product
from service.models import Service
from source_utils.starters import CommonInfo


class Order(CommonInfo):
    """ This model represents an order created for a customer. """
    client = models.ForeignKey(
        User,
        related_name='work_order_client', 
        limit_choices_to={'is_staff': False}, 
        on_delete=models.CASCADE
    )
    description = models.CharField(
        "Job description", 
        max_length=30
    )
    note = models.TextField(
        max_length=300, 
        blank=True, 
        null=True
    )
    services = models.ManyToManyField(
        'service.Service', 
        blank=True
    )   
    sent_to_finance = models.BooleanField(
        default=False
    )
    scheduled = models.DateTimeField(
        "Product scheduled", 
        blank=True, 
        null=True
    )
    time_requirements_filled = models.BooleanField(
        default=False
    )
    pulled = models.DateTimeField(
        "Product pulled", 
        blank=True, 
        null=True
    )
    work_initiated = models.DateTimeField(
        blank=True, 
        null=True
    )   
    work_completed = models.DateTimeField(
        blank=True, 
        null=True
    )      
    closed_out = models.DateTimeField(
        blank=True, 
        null=True
    )
    postponed = models.DateTimeField(
        "Service postponed", 
        blank=True, 
        null=True
    )    
    job_history = models.TextField(
        default = '', 
        max_length=30000, 
        blank=True, 
        null=True
    ) 


    class Meta:
        ordering = ["origin", "client"]
        unique_together = ("client", "description")

    def __str__(self):
        return "{} - {} ({})".format(
            self.client.full_family_name(), 
            self.description, 
            self.origin.strftime("%Y-%m-%d")
        )

    def get_services_parts_time_cost_list(self):
        all_time = 0
        all_cost = 0
        parts_list = ""

        for service in self.services.all():
            time, cost, parts = service.get_parts_time_cost_list()
            all_time += time
            all_cost += cost
            parts_list += parts
        return all_time, all_cost, parts_list

    def check_for_close_out(self):
        if self.work_completed and not self.postponed and self.sent_to_finance \
            and self.work_initiated and self.pulled and self.scheduled:
            return True
        return False

    def get_absolute_url(self):
        return reverse("work_order:order_detail", kwargs={"slug": self.slug})

    def get_service_list(self):
        return '\n'.join([s.service_description for s in self.services.all()])


def pre_save_order(sender, instance, *args, **kwargs):
    slug = "{} - {} ({})".format(
        instance.client.full_family_name(), 
        instance.description, 
        str(datetime.date.today())
    )
    instance.slug = slugify(slug)

pre_save.connect(pre_save_order, sender=Order)
