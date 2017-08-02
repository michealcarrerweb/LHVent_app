from __future__ import unicode_literals

from datetime import datetime, timedelta
from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy, reverse

from company.models import Company
from source_utils.starters import CommonInfo, Conflict
from versatileimagefield.fields import (
    VersatileImageField, PPOIField
)
# from model_utils import FieldTracker


UPDATE_OPTION = (
        ('Payment', 'Payment(-)'),
        ('Discount', 'Discount(-)'),
        ('Fee', 'Fee/Additional Cost(+)'),  
        ('Error-Add', 'Add to previous entry amount due to \
            under error entry(-)'),
        ('Error-Off', 'Take from previous entry amount due \
            to over error entry(+)'),
    )


class Invoice(CommonInfo):
    vendor = models.ForeignKey(
        'company.Company', 
        on_delete=models.CASCADE
    )
    plu = models.CharField(
        "Invoice ID",
        unique=True, 
        max_length=60
    )
    invoice_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2
    )
    due_by = models.DateField(
        blank=True, 
        null=True
    )
    note = models.CharField(
        max_length=300,
        blank=True, 
        null=True
    )
    paid_in_full = models.BooleanField(
        default=False
    )
    over_paid = models.BooleanField(
        default=False
    )
    file = models.FileField(
        'File',
        upload_to='uploads/operations_invoice/',
        null=True, 
        blank=True,
    )
    image = VersatileImageField(
        'Image',
        upload_to='images/operations_invoice/',
        null=True, 
        blank=True,
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
    log = models.TextField(
        default = '', 
        max_length=30000, 
        blank=True, 
        null=True
    )

    class Meta:
        unique_together = ("vendor", "plu")

    def __str__(self):
        identifier = "{}-{}".format(
            self.origin.strftime("%y"),
            self.pk
        )
        return "{} {} - ({})".format(
            self.vendor, 
            self.plu,
            identifier
        )

    def get_absolute_url(self):
        return reverse(
            "operation_finance:invoice_detail", 
            kwargs={'slug': self.slug}
        )

    def get_payment_schedule(self):       
        total_alterations = InvoiceAlteration.objects.filter(invoice=self)
        if total_alterations:
            payment_schedule = ""
            for item in total_alterations:
                payment_schedule += "{} of ${} was added on {}\n".format( 
                    item.transaction_update,
                    item.transaction_amount,
                    item.origin.strftime(
                                "%Y-%m-%d %H:%M:%S")                       
                )
                if item.transaction_note:
                    payment_schedule = "{} - {}\n".format(
                        payment_schedule,
                        item.transaction_note
                    )
            return payment_schedule
        else:
            return "No payments" 

    def get_balance_due(self):
        total_alterations = InvoiceAlteration.objects.filter(invoice=self)
        if total_alterations:
            payments = 0
            for item in total_alterations:
                payments += item.transaction_amount
            balance_due = self.invoice_amount - payments
            if balance_due == 0:
                self.paid_in_full = True
                self.over_paid = False
            elif balance_due > 0:
                self.paid_in_full = False
                self.over_paid = False
            else:
                self.paid_in_full = False
                self.over_paid = True 
            self.save()         
            return balance_due
        else:
            return self.invoice_amount


def pre_save_operation_financial(sender, instance, *args, **kwargs):
    slug = "{}{}-{}".format(
        instance.vendor,
        instance.plu,
        datetime.now().strftime("%y")
    )
    instance.slug = slugify(slug)

pre_save.connect(pre_save_operation_financial, sender=Invoice)


class VendorConflict(Conflict):
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='conflict'
    )

    def get_absolute_url(self):
        return reverse(
            "operation_finance:conflict_update", 
            kwargs={'pk': self.pk}
        )

    class Meta:
        unique_together = ("invoice", "conflict_description")

    def __str__(self):
        return self.invoice.__str__()


class InvoiceAlteration(CommonInfo):
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='bill'
    )
    transaction_update = models.CharField(
        max_length=30,
        choices=UPDATE_OPTION
    )
    transaction_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2
    )
    transaction_note = models.CharField(
        max_length=100, 
        blank=True, 
        null=True
    )

    class Meta:
        verbose_name = _('Alteration')
        verbose_name_plural = _('Alterations')

    def __init__(self, *args, **kwargs):
        super(InvoiceAlteration, self).__init__(*args, **kwargs)
        self.note = ""    

    def __str__(self):
        return "{} - ({})".format(
            self.transaction_update,
            str(self.pk)
        )

    def get_absolute_url(self):
        return reverse(
            "operation_finance:invoice_detail", 
            kwargs={'slug': self.invoice.slug}
        )

    def save(self, *args, **kwargs):
        if self.transaction_update == 'Fee' or \
                    self.transaction_update == 'Error-Off':
            self.transaction_amount = -abs(self.transaction_amount) 
        return super(InvoiceAlteration, self).save(*args, **kwargs)
