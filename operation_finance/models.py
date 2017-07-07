from __future__ import unicode_literals

from datetime import datetime, timedelta
from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404, render, redirect

from source_utils.starters import CommonInfo
from versatileimagefield.fields import (
    VersatileImageField, PPOIField
)
from model_utils import FieldTracker


UPDATE_OPTION = (
        ('Paid', 'Payment'), 
        ('Cost', 'Additional Cost'), 
        ('Credit', 'Company Reimbursement'), 
    )

DAYS_OUT = datetime.now()+timedelta(days=25)


def upload_location(instance, filename):
    return "%s/%s" %(instance.slug, filename)


class Invoice(CommonInfo):
    invoice = models.CharField(
        "Invoice description", 
    	max_length=200
    )
    plu = models.CharField(
        "Invoice ID",
        unique=True, 
        max_length=30,
        blank=True, 
        null=True
    )
    # ledger = models.ForeignKey(
    #     'finance.Ledger', 
    #     limit_choices_to={'revenue':False},
    # 	on_delete=models.CASCADE
    # )
    invoice_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2
    )
    due_by = models.DateField(
        default = DAYS_OUT
    )
    conflict = models.BooleanField(
        default=False
    )
    conflict_description = models.CharField(
        "Conflict description/resolution",
        null=True, 
        blank=True, 
        max_length=300
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
    image = VersatileImageField(
        'Image',
        upload_to='images/operations_invoice/',
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
    conflict_tracker = FieldTracker(
        fields=['conflict',]
    )
    log = models.TextField(
        default = '', 
        max_length=30000, 
        blank=True, 
        null=True
    )

    class Meta:
        unique_together = ("invoice", "plu")

    def __init__(self, *args, **kwargs):
        super(Invoice, self).__init__(*args, **kwargs)
        self.plu_id = ""
        self.extra = 0
        self.balance = 0
        self.payments = 0
        self.payment_schedule = ""

    def __str__(self):
        if self.plu:
            self.plu_id = " {}".format(self.plu)
        return "{}{} - ({})".format(
            self.invoice, 
            self.plu_id,
            self.origin.date()
        )

    def get_absolute_url(self):
        return reverse(
            "operation_finance:invoice_detail", 
            kwargs={'slug': self.slug}
        )

    def get_balance(self):
        invoice = Invoice.objects.get(id=self.id)
        total_alterations = invoice.bill.all()
        for item in total_alterations:
            self.payment_schedule += "${} of {} was added on {}\n".format(
                item.transaction_amount, 
                item.transaction_update,
                item.origin
            )
            if item.transaction_update == 'Cost':
                item.transaction_amount = -abs(item.transaction_amount)
            self.payments += item.transaction_amount
        self.balance = self.invoice_amount - self.payments
        if self.balance < 0:
            self.paid_in_full = False
            self.over_paid = True
        elif self.balance == 0:
            self.paid_in_full = True
            self.over_paid = False
        else:
            self.paid_in_full = False
            self.over_paid = False           
        self.save()

    def save(self, *args, **kwargs):
        if self.conflict_tracker.has_changed('conflict'):
            if self.conflict_tracker.previous('conflict') == False:
                self.log += "Conflict arose on {}\n".format(
                        str(datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"))
                        )
                if self.conflict_description:
                    self.log += "\t- reason: {}\n".format(
                        self.conflict_description)
                    self.conflict_description = ""
            elif self.conflict_tracker.previous('conflict') == True:
                self.log += "Conflict resolved on {}\n".format(
                        str(datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"))
                        )
                if self.conflict_description:
                    self.log += "\t- resolution: {}\n".format(
                                    self.conflict_description)
                    self.conflict_description = ""
        return super(Invoice, self).save(*args, **kwargs)


def pre_save_operation_financial(sender, instance, *args, **kwargs):
    if instance.plu:
            instance.plu_id = " {}".format(instance.plu)
    financial_name = "{}{} - {}".format(
        instance.invoice,  
        instance.plu_id,
        instance.origin#.date()
    )
    instance.slug = slugify(financial_name)

pre_save.connect(pre_save_operation_financial, sender=Invoice)


class InvoiceAlteration(CommonInfo):
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='bill'
    )
    plu = models.CharField(
        "Payment ID",
        unique=True, 
        max_length=30,
        blank=True, 
        null=True
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

    def __init__(self, *args, **kwargs):
        super(InvoiceAlteration, self).__init__(*args, **kwargs)
        self.plu_id = ""    

    def __str__(self):
        if self.plu:
            self.plu_id = " {}".format(self.plu)
        return "{}{} - ({})".format(
            self.invoice, 
            self.plu_id,
            self.origin
        )

    def get_absolute_url(self):
        return reverse(
            "operation_finance:invoice_detail", 
            kwargs={'slug': self.invoice.slug}
        )


def pre_save_invoice_alteration(sender, instance, *args, **kwargs):
    if instance.invoice.plu:
            instance.plu_id = " {}".format(instance.invoice.plu)
    alteration = "{}{} - {}/{}/{}".format(
        instance.invoice.invoice, 
        instance.invoice.plu_id,
        instance.invoice.origin,
        instance.transaction_update,
        instance.transaction_amount
    )
    instance.slug = slugify(alteration)

pre_save.connect(pre_save_invoice_alteration, sender=InvoiceAlteration)
