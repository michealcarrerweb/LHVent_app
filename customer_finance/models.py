from __future__ import unicode_literals

import datetime
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404, render, redirect

from hourly.models import Hourly
from service.models import PartsForService
from source_utils.starters import CommonInfo, Conflict

from model_utils import FieldTracker

UPDATE_OPTION = (
        ('Payment', 'Payment(-)'),
        ('Refund', 'Refund(+)'),
        ('Fee', 'Fee/Additional Cost(-)'),
        ('Discount', 'Discount(+)'), 
        ('Error-Add', 'Add to previous entry amount due to \
            under error entry(-)'),
        ('Error-Off', 'Take from previous entry amount due \
            to over error entry(+)'),
    )


class Invoice(CommonInfo):
    work_order = models.OneToOneField(
        'work_order.Order', 
        related_name='work_order_invoice',
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
    due_by = models.DateField(
        blank=True, 
        null=True
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

    def __str__(self):
        return "{} - {} ({})".format(
            self.work_order.client.full_family_name(), 
            self.work_order.description,
            self.work_order.origin.strftime("%Y-%m-%d"))

    def get_absolute_url(self):
        return reverse(
            "customer_finance:invoice_detail", 
            kwargs={'slug': self.slug}
        )

    def check_for_conflicts(self):
        return self.conflict.filter(conflict_resolution=None)                

    def get_quote(self):
        try:
            quote = PriceQuote.objects.get(invoice=self)
        except PriceQuote.DoesNotExist:
            quote = PriceQuote(invoice=self, total_price_quoted=0.00, tax_on_quote=0.00)
            quote.save()
        return quote

    def check_for_close_out(self):
        if self.paid_in_full and not self.over_paid and self.work_order.check_for_close_out():
            for conflicts in self.conflict.all():
                if not conflicts.conflict_resolution:
                    print("a")
                    return False
            print("b")
            return True
        else:
            print("ds")
            return False

    def get_cost(self):
        time, cost, parts = self.work_order.get_services_parts_time_cost_list()
        mark_up_value = Decimal(
            (self.pricing.percentage / 100.00) + 1
        )
        before_tax =  cost * mark_up_value
        taxes = Decimal(self.tax) / 100
        total_tax = before_tax * taxes
        total_after_tax = before_tax + total_tax
        return total_after_tax, before_tax, total_tax

    def get_balance_due(self):
        total_alterations = InvoiceAlteration.objects.filter(invoice=self)
        if total_alterations:
            balance_due = 0
            payments = 0
            for item in total_alterations:
                payments += item.transaction_amount
            try:
                quote = self.get_quote()
                balance_due = quote.total_price_quoted - payments
                if balance_due < 0:
                    self.paid_in_full = False
                    self.over_paid = True
                elif balance_due == 0:
                    self.paid_in_full = True
                    self.over_paid = False
                else:
                    self.paid_in_full = False
                    self.over_paid = False 
                self.save()
            except PriceQuote.DoesNotExist:
                balance_due = -abs(payments)         
            return balance_due
        else:
            try:
                balance_due = self.invoice_quote.total_price_quoted
                return balance_due
            except:
                return "Not quoted yet"

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

    def save(self, *args, **kwargs):
        super(Invoice, self).save(*args, **kwargs)
        quote = self.get_quote()
        if self.give_price_quote:
            total_after_tax, before_tax, total_tax = self.get_cost()
            if "{0:0.1f}".format(total_after_tax) != "{0:0.1f}".format(
                    quote.total_price_quoted) and quote.total_price_quoted != 0.00:
                self.log += "Price quote modified to ${} on {}\n".format(
                        round(total_after_tax, 2),
                        quote.last_modified.strftime(
                            "%Y-%m-%d %H:%M:%S")
                        )
            elif quote.total_price_quoted == 0.00:
                self.log += "Price quote of ${} added on {}\n".format(
                        round(total_after_tax, 2),
                        quote.origin.strftime(
                            "%Y-%m-%d %H:%M:%S")
                )
            quote.total_price_quoted = total_after_tax
            quote.tax_on_quote = total_tax
            quote.save()
            self.give_price_quote = False
            self.save()
        if self.closed_out:
            if not self.paid_in_full or self.over_paid or not \
                self.work_order.closed_out or not self.invoice_quote:
                self.closed_out = False
                self.save()
        # else:
        #     self.log += "Invoice closed out on {} by {}\n".format(
        #         datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        #         request.user,
        #         )
        #     self.save()       
        if self.work_order.sent_to_finance == False:
            self.work_order.sent_to_finance = True
            self.work_order.save()


def pre_save_project_financial(sender, instance, *args, **kwargs):
    financial_name = "{} - {}({})".format(
        instance.work_order.client.full_family_name(),
        instance.work_order.description,
        str(datetime.date.today())
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
        funds_back = ('Refund', 'Discount', 'Error-Off')
        if self.transaction_update in funds_back:
            self.transaction_amount = -abs(self.transaction_amount) 
        return super(InvoiceAlteration, self).save(*args, **kwargs)
