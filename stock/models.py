from __future__ import unicode_literals

from django.db import models
import datetime

from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from source_utils.starters import CommonInfo, GenericCategory
from versatileimagefield.fields import (
    VersatileImageField, 
    PPOIField
)


def upload_location(instance, filename):
    return "%s/%s" %(instance.slug, filename)


ASSESEMENT = (
        ('units', 'Per unit'),
        ('square feet', 'Square foot'),
        ('linear feet', 'Linear foot'),
        ('square meters', 'Square meter'),
        ('linear meters', 'Linear meter'),
    )


class Base(GenericCategory):
    """ 
    This model represents the general type of product category offered. 
    """
    class Meta:
        verbose_name = _('Product Category')
        verbose_name_plural = _('Product Categories')
        ordering = ["category"]

    def get_success_url(self):
        return reverse("product:company_list")

    def get_absolute_url(self):
        return reverse(
                    "product:base_product_detail", 
                    kwargs={'slug': self.slug}
                    )


def pre_save_category(sender, instance, *args, **kwargs):

    instance.slug = slugify(instance.category)

pre_save.connect(pre_save_category, sender=Base)


class Product(CommonInfo):
    """ 
    This model describes the specific product related to the category. 
    """
    base = models.ForeignKey(
        Base, 
        on_delete=models.CASCADE
    )
    supplier = models.ForeignKey(
        'company.Company', 
        on_delete=models.CASCADE
    )
    item = models.CharField(
        max_length=30, 
        unique=True
    )
    admin_time = models.DecimalField(
        default=0, 
        max_digits=4, 
        decimal_places=2
    )
    prep_time = models.DecimalField(
        default=0, 
        max_digits=4, 
        decimal_places=2
    )
    field_time = models.DecimalField(
        default=0,
        max_digits=4, 
        decimal_places=2
    )
    admin_material = models.DecimalField(
        default=0, 
        max_digits=8, 
        decimal_places=2
    )
    prep_material = models.DecimalField(
        default=0, 
        max_digits=8, 
        decimal_places=2
    )
    field_material = models.DecimalField(
        default=0, 
        max_digits=8, 
        decimal_places=2
    )
    quantity_assesement = models.CharField(
        max_length=12, 
        verbose_name=_("Quantity assesement method"), 
        choices=ASSESEMENT
    )
    order_if_below = models.SmallIntegerField()
    discontinued = models.DateField(
        null=True, 
        blank=True
    )
    order_now = models.BooleanField(
        default=False
    )
    units_damaged_or_lost = models.SmallIntegerField(
        default=0
    )
    quantity = models.SmallIntegerField(
        "Usable quantity",
        default=0, 
        null=True, 
        blank=True
    )
    quantity_called_for = models.SmallIntegerField(
        default=0, 
        null=True, 
        blank=True
    )
    image = VersatileImageField(
        'Image',
        upload_to='images/product/',
        null=True, blank=True,
        width_field='width',
        height_field='height',
        ppoi_field='ppoi'
    )
    height = models.PositiveIntegerField(
        'Image Height',
        blank=True,
        null=True
    )
    width = models.PositiveIntegerField(
        'Image Width',
        blank=True,
        null=True
    )
    ppoi = PPOIField(
        'Image PPOI'
    )
    no_longer_available = models.BooleanField(default=False)

    class Meta:
        ordering= ['item']

    def __str__(self):
        return self.item

    def get_time(self):
        return self.admin_time + self.prep_time + self.field_time

    def get_cost(self):
        return self.admin_material + self.prep_material + self.field_material

    def get_usable_quantity(self):
        return self.quantity - self.units_damaged_or_lost - self.quantity_called_for

    def get_success_url(self):
        return reverse("product:category_item_list", kwargs={'slug': self.base.slug})

    def get_absolute_url(self):
        return reverse("product:item_detail", kwargs={'slug': self.slug})


def pre_save_product(sender, instance, *args, **kwargs):

    if not instance.no_longer_available:
        instance.discontinued = None
    elif instance.no_longer_available and instance.discontinued == None:
        instance.discontinued = datetime.date.today()
    if (
        instance.quantity - 
        instance.units_damaged_or_lost - 
        instance.quantity_called_for
            ) < instance.order_if_below:
        instance.order_now = True
    else:
        instance.order_now = False
    instance.slug = slugify(instance.item)
     
pre_save.connect(pre_save_product, sender=Product)