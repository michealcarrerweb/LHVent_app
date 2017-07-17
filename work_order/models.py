from __future__ import unicode_literals

import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404

from stock.models import Product
from service.models import Service, PartsForService

from model_utils import FieldTracker


class Order(models.Model):
    """ This model represents an order created for a customer. """
    slug = models.SlugField(
        blank=True
    )
    client = models.ForeignKey(
        User, 
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
    scheduled = models.BooleanField(
        default=False
    )
    sent_to_finance = models.BooleanField(
        default=False
    )
    postponed = models.BooleanField(
        verbose_name="Order postponed", 
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
    order_created = models.DateField(
        auto_now_add=True
    )      
    closed_out = models.DateTimeField(
        blank=True, 
        null=True
    )    
    job_history = models.TextField(
        default = '', 
        max_length=30000, 
        blank=True, 
        null=True
    ) 

    order_tracker = FieldTracker(
        fields=['client', 'description', 'postponed', 'pulled', 'work_completed']
    )

    class Meta:
        ordering = ["order_created", "client"]
        unique_together = ("client", "description")

    def __init__(self, *args, **kwargs):
        super(Order, self).__init__(*args, **kwargs)
        self.all_time = 0
        self.all_cost = 0
        self.parts_list = ""
        self.services_list = ""

    def __str__(self):
        name = self.client.first_name
        if self.client.account.spouse_name:
            name += " and " + self.client.account.spouse_name
        return "{} {} - {} ({})".format(
            name, self.client.last_name, self.description, self.order_created
        )

    def get_services_parts_time_cost_list(self):

        for service in self.services.all():
            time, cost, parts = service.get_parts_time_cost_list()
            self.all_time += time
            self.all_cost += cost
            self.parts_list += parts
        # print(self.all_time, self.all_cost, self.parts_list)
        return self.all_time, self.all_cost, self.parts_list

    def get_absolute_url(self):
        return reverse("work_order:order_detail", kwargs={"slug": self.slug})

    def get_service_list(self):
        return '\n'.join([s.service_description for s in self.services.all()])


def pre_save_order(sender, instance, *args, **kwargs):
    spouse = ""
    if instance.client.account.spouse_name:
        spouse = " and " + instance.client.account.spouse_name
    slug = (
        instance.client.first_name + spouse + " " + 
        instance.client.last_name + " - " + instance.description + " " + 
        str(datetime.date.today())
    )
    instance.slug = slugify(slug)
    instance.last_modified = timezone.now()
    items = instance.order_tracker.changed()
    for item in items:
        if items[item] != None:
            new_log = "{} altered from {} on {}\n".format(
                item, items[item], datetime.datetime.today()
            )
            instance.job_history += new_log

pre_save.connect(pre_save_order, sender=Order)
