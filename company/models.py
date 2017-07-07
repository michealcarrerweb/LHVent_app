from __future__ import unicode_literals

from django.db import models

from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from source_utils.starters import CommonInfo, GenericCategory


class Company(CommonInfo):
    """ 
    This model represents the company that provides product. 
    """
    company = models.CharField(
        max_length=30, 
        unique=True
    )
    address = models.CharField(
        max_length=120
    )
    company_phone = models.CharField(
        max_length=30,
        null=True, 
        blank=True
    )
    no_longer_use = models.BooleanField(
        default=False
    )

    class Meta:
        verbose_name = _('Supplier')
        verbose_name_plural = _('Suppliers')
        ordering = ["company"]

    def __str__(self):
        return self.company

    def get_success_url(self):
        return reverse("product:company_list")

    def get_absolute_url(self):
        return reverse("product:company_detail", kwargs={'slug': self.slug})


def pre_save_company(sender, instance, *args, **kwargs):

    instance.slug = slugify(instance.company)

pre_save.connect(pre_save_company, sender=Company)


class Contact(models.Model):
    """ 
    This model describes the contact related to the company. 
    """
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='company_contact'
    )
    contact_name = models.CharField(
        max_length=30
    )
    contact_position = models.CharField(
        max_length=30
    )
    phone = models.CharField(
        max_length=30
    )
    email = models.EmailField(
        max_length=30
    )
