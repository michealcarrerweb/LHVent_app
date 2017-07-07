from __future__ import unicode_literals

from django.db import models

from django.db.models.signals import pre_save
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from source_utils.starters import CommonInfo, GenericCategory
from hourly.models import Hourly
from pinax.eventlog.models import Log


class Base(GenericCategory):
    """ 
    This model represents the general type of service category offered. 
    """
    class Meta:
        verbose_name = _('Base')
        verbose_name_plural = _('Base')
        ordering = ["category"]

    def get_success_url(self):
        return reverse(
            "product:company_list"
            )

    def get_absolute_url(self):
        return reverse(
            "service:base_service_detail", 
            kwargs={'slug': self.slug}
            )


def pre_save_category(sender, instance, *args, **kwargs):

    instance.slug = slugify(instance.category)

pre_save.connect(pre_save_category, sender=Base)


class Service(CommonInfo):
    """ This model describes a specific service. """

    base = models.ForeignKey(
        Base, 
        on_delete=models.CASCADE
    )
    service_description = models.CharField(
        max_length=30, 
        unique=True
    )
    job_tools = models.ManyToManyField(
        'equipment.JobTool',
        limit_choices_to={'base__gt':1},
        blank=True
    )
    additional_hours = models.DecimalField(
        default = 0, 
        max_digits=5, 
        decimal_places=2,
        null=True, 
        blank=True
    )
    hourly_additional = models.SmallIntegerField(
        default = 0,
        null=True, 
        blank=True
    )
    service_no_longer_available = models.BooleanField(
        default=False
    )

    def __init__(self, *args, **kwargs):
        super(Service, self).__init__(*args, **kwargs)
        self.all_time = 0
        self.all_cost = 0
        self.parts_list = ""

    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')
        ordering= ['base', 'service_description']

    def __str__(self):
        return self.service_description

    def get_absolute_url(self):
        return reverse("service:service_detail", kwargs={'slug': self.slug})

    def get_parts_time_cost_list(self):
        hourly_rate = get_object_or_404(Hourly, pk=1)
        hourly_base = hourly_rate.hourly_base
        if self.hourly_additional:
            hourly_base += self.hourly_additional
        serve = Service.objects.get(slug=self.slug)
        self.all_time = self.additional_hours
        for part in serve.parts.all():
            ending = "\n"
            if part.product.no_longer_available:
                ending = " - !! PART NO LONGER AVAILABLE !!\n"
            elif part.product.quantity <= 0:
                ending = " - !! PART OUT OF STOCK !!\n"
            description = "{} {} - {}{}".format(
                str(part.quantity),
                part.product.quantity_assesement,
                part.product.item,
                ending
            )
            self.parts_list += description
            part_tot_time = (part.product.get_time() * part.quantity)
            self.all_time += part_tot_time
            part_tot_cost = (part.product.get_cost() * part.quantity)
            self.all_cost += part_tot_cost
        hourly_cost = self.all_time * hourly_base
        self.all_cost += hourly_cost
        return self.all_time, self.all_cost, self.parts_list

    def get_job_tools(self):
        return '\n'.join([t.tool for t in self.job_tools.all()])   

def pre_save_service(sender, instance, *args, **kwargs):
    instance.slug = slugify(instance.service_description)

pre_save.connect(pre_save_service, sender=Service)


class PartsForService(models.Model):
    """ This model represents the parts and quantity needed for an aspect 
        of a service. """

    service = models.ForeignKey(
        Service, 
        on_delete=models.CASCADE,
        related_name='parts'
    )
    product = models.ForeignKey(
        'stock.Product'
    )
    quantity = models.DecimalField(
        default=1, 
        max_digits=7, 
        decimal_places=2,
        blank=True
    )
    description = models.CharField(
        max_length=30,
        null=True, 
        blank=True
    )

    class Meta:
        ordering = ["description"]

    def __str__(self):
        return "{}'s {}".format(
            self.service.service_description, 
            self.description
        )
