from __future__ import unicode_literals

import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from source_utils.starters import CommonInfo, GenericCategory


CONDITION = (
        ('good', 'Usable'),
        ('damaged', 'Damaged'),
        ('lost', 'Lost'),
        ('sent out for repair', 'Out for repair'),
)


TOOL_TYPE = (
        ('personal', 'Personal'),
        ('company', 'Company'),
        ('rental', 'Rental'),
)


class Base(GenericCategory):
    """ 
    This model represents the general type of tool category offered. 
    """
    class Meta:
        verbose_name = _('equipment Category')
        verbose_name_plural = _('equipment Categories')
        ordering = ["category"]

    def get_success_url(self):
        return reverse("product:company_list")

    def get_absolute_url(self):
        return reverse(
                    "equipment:base_detail", 
                    kwargs={'slug': self.slug}
                    )


def pre_save_category(sender, instance, *args, **kwargs):

    instance.slug = slugify(instance.category)

pre_save.connect(pre_save_category, sender=Base)


class JobTool(CommonInfo):
    """ 
    This model describes the specific tool related to the category. 
    """

    base = models.ForeignKey(
        Base, 
        on_delete=models.CASCADE
    )
    supplier = models.ForeignKey(
        'company.Company', 
        on_delete=models.CASCADE
    )
    tool = models.CharField(
        max_length=30, 
        unique=True
    )
    tool_type = models.CharField(
        max_length=10, 
        choices=TOOL_TYPE,
        default=CONDITION[1][1]
    )
    initial_usage = models.DateField(
        auto_now_add=True
    )
    condition = models.CharField(
        max_length=20, 
        choices=CONDITION,
        default=CONDITION[0][0]
    )
    incident = models.DateField(
        null=True, 
        blank=True
    )

    class Meta:
        ordering= ['tool']

    def __str__(self):
        return self.tool

    def get_absolute_url(self):
        return reverse("equipment:job_tool_detail", kwargs={'slug': self.slug})

    def is_condition(self):
        return self.condition


def pre_save_tool(sender, instance, *args, **kwargs):

    if instance.condition == 'good':
        instance.incident = None
    elif instance.incident:
        instance.incident = instance.incident
    else:
        instance.incident = datetime.date.today()
    instance.slug = slugify(instance.tool)

pre_save.connect(pre_save_tool, sender=JobTool)

