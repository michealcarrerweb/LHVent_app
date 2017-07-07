from __future__ import unicode_literals

import datetime
from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404, render, redirect

# from finance.models import PriceQuote
from hourly.models import Hourly
from service.models import PartsForService
from source_utils.starters import CommonInfo, Conflict

from model_utils import FieldTracker

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
    work_order = models.OneToOneField(
        'work_order.Order', 
        limit_choices_to={'sent_to_finance':False},
        on_delete=models.CASCADE
    )
    pricing = models.ForeignKey(
        'finance.Pricing', 
        on_delete=models.CASCADE
    )
    tax = models.DecimalField(
        default=6.0, 
        max_digits=4, 
        decimal_places=2
    )
    give_price_quote = models.BooleanField(
        default=False
    )
    paid_in_full = models.BooleanField(
        default=False
    )
    over_paid = models.BooleanField(
        default=False
    )
    closed_out = models.BooleanField(
        default=False
    )
    note = models.CharField(
        null=True, 
        blank=True, 
        max_length=300
    )
    log = models.TextField(
        default = '', 
        max_length=30000, 
        blank=True, 
        null=True
    )

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')
        ordering = ["-origin", "work_order"]

    def __init__(self, *args, **kwargs):
        super(Invoice, self).__init__(*args, **kwargs)
        self.all_time = 0
        self.all_cost = 0
        self.before_tax = 0
        self.total_after_tax = 0
        self.total_tax = 0
        self.balance_due = 0
        self.payments = 0
        self.payment_schedule = ""

    def __str__(self):
        name = self.work_order.client.first_name
        if self.work_order.client.spouse_name:
            name += " and " + self.work_order.client.spouse_name
        return "{} {} - {} ({})".format(
            name,
            self.work_order.client.last_name, 
            self.work_order.description,
            self.work_order.order_created)

    def get_absolute_url(self):
        return reverse(
            "customer_finance:invoice_detail", 
            kwargs={'slug': self.slug}
        )

    def get_quote(self):
        return PriceQuote.objects.get(invoice=self)

    def get_cost(self):
        hourly_rate = get_object_or_404(Hourly, pk=1)
        hourly_base = hourly_rate.hourly_base
        for service in self.work_order.services.all():
            print(service)
            self.all_time += service.additional_hours
            hourly_base += service.hourly_additional
            parts_list = PartsForService.objects.filter(service=service)
            for part in parts_list:
                self.all_time += part.product.get_time()
                self.all_time *= hourly_base
                mark_up_value = Decimal(
                    (self.pricing.percentage / 100.00) + 1
                )
                self.all_time *= mark_up_value
                self.all_cost += part.product.get_cost()
                self.all_cost *= mark_up_value
        self.before_tax = (self.all_time + self.all_cost)
        taxes = Decimal(self.tax) / 100
        self.total_tax = self.before_tax * taxes
        self.total_after_tax = self.before_tax + self.total_tax
        # return self.before_tax

    def get_balance_due(self):
        # invoice = Invoice.objects.get(id=self.id)
        total_alterations = InvoiceAlteration.objects.filter(invoice=self)
        print(total_alterations)
        if total_alterations:
            for item in total_alterations:
                self.payment_schedule += "{} of ${} was added on {}\n".format( 
                    item.transaction_update,
                    item.transaction_amount,
                    item.origin.strftime(
                                "%Y-%m-%d %H:%M:%S")                       
                )
                # if item.transaction_update == 'Fee' or \
                #         item.transaction_update == 'Error-Off':
                #     item.transaction_amount = -abs(item.transaction_amount)
                self.payments += item.transaction_amount
            try:
                quote = self.get_quote()
                self.balance_due = quote.total_price_quoted - self.payments
                # if self.balance_due < 0:
                #     self.paid_in_full = False
                #     self.over_paid = True
                # elif self.balance_due == 0:
                #     self.paid_in_full = True
                #     self.over_paid = False
                # else:
                #     self.paid_in_full = False
                #     self.over_paid = False 
            except PriceQuote.DoesNotExist:
                self.balance_due = None          
            # self.save()
        #     return self.balance_due
        # else:
        #     return self.invoice_quote.total_price_quoted

    def save(self, *args, **kwargs):
        before_tax = self.get_cost()
        if self.give_price_quote:
            try:
                quote = self.get_quote()
                if "{0:0.1f}".format(self.total_after_tax) != "{0:0.1f}".format(
                        quote.total_price_quoted):
                    self.log += "Price quote modified to ${} on {}\n".format(
                            round(self.total_after_tax, 2),
                            quote.last_modified.strftime(
                                "%Y-%m-%d %H:%M:%S")
                            )
                    quote.total_price_quoted = self.total_after_tax
                    quote.tax_on_quote = self.total_tax
                    quote.save()
            except PriceQuote.DoesNotExist:
                quote = PriceQuote(
                    invoice=self, 
                    total_price_quoted=self.total_after_tax, 
                    tax_on_quote=self.total_tax
                )
                quote.save()
                self.log += "Price quote of ${} added on {}\n".format(
                        round(quote.total_price_quoted, 2),
                        quote.origin.strftime(
                            "%Y-%m-%d %H:%M:%S")
                )
        self.give_price_quote = False
        if self.work_order.sent_to_finance == False:
            self.work_order.sent_to_finance = True
            self.work_order.save()

        return super(Invoice, self).save(*args, **kwargs)


def pre_save_project_financial(sender, instance, *args, **kwargs):
    spouse = " and "
    if instance.work_order.client.spouse_name:
        spouse = spouse + instance.work_order.client.spouse_name
    else:
            spouse = ""
    num = str(instance.pk)
    if len(num) < 5:
        while len(num) < 5:
            num = "0" + num
    financial_name = "{} {} {} - {}".format(
        instance.work_order.client.first_name, 
        spouse, 
        instance.work_order.client.last_name,
        num
    )
    instance.slug = slugify(financial_name)

pre_save.connect(pre_save_project_financial, sender=Invoice)


class PriceQuote(CommonInfo):
    
    invoice = models.OneToOneField(
        Invoice,
        on_delete=models.CASCADE,
        related_name='invoice_quote'
    )
    total_price_quoted = models.DecimalField(
        null=True, 
        blank=True,
        max_digits=10, 
        decimal_places=2
    )
    tax_on_quote = models.DecimalField(
        null=True, 
        blank=True,
        max_digits=9, 
        decimal_places=2
    )


class CustomerConflict(Conflict):
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='conflict'
    )

    def get_absolute_url(self):
        return reverse(
            "customer_finance:conflict_update", 
            kwargs={'slug': self.slug}
        )

    def __str__(self):
        return self.invoice.__str__()

def pre_save_conflict(sender, instance, *args, **kwargs):
    conflict = "{}-{}".format(
        instance.invoice.slug,
        instance.origin
    )
    instance.slug = slugify(conflict)

pre_save.connect(pre_save_conflict, sender=CustomerConflict)


class InvoiceAlteration(CommonInfo):
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='invoice'
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
            "customer_finance:invoice_detail", 
            kwargs={'slug': self.invoice.slug}
        )

    def save(self, *args, **kwargs):
        if self.transaction_update == 'Fee' or \
                    self.transaction_update == 'Error-Off':
            self.transaction_amount = -abs(self.transaction_amount) 
        if self.transaction_note:
            self.note = ", reason: " + self.transaction_note
        # self.invoice.save()
        return super(InvoiceAlteration, self).save(*args, **kwargs)

def pre_save_invoice_alteration(sender, instance, *args, **kwargs):
    alteration = "{}-{}/{}/{}/{}".format(
        instance.invoice.work_order.client.last_name, 
        instance.invoice.work_order.description,
        instance.transaction_update,
        instance.transaction_amount,
        str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    instance.slug = slugify(alteration)

pre_save.connect(pre_save_invoice_alteration, sender=InvoiceAlteration)
