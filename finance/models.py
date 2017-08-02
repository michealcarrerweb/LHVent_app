from __future__ import unicode_literals

from django.db import models
import datetime

from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from customer_finance.models import (
    Invoice as Customer_Invoice,
    CustomerConflict,
    )

from operation_finance.models import (
    Invoice as Operation_Invoice,
    VendorConflict,
    )
from service.models import PartsForService
from source_utils.starters import CommonInfo

from model_utils import FieldTracker


class Pricing(models.Model):
    slug = models.SlugField(
        null=True, 
        blank=True
    )
    pricing = models.CharField(
        unique=True, 
        max_length=30
    )
    percentage = models.IntegerField() 

    class Meta:
        verbose_name_plural = _('Pricing')
        ordering = ["percentage"]

    def __str__(self):
        return self.pricing

    def get_absolute_url(self):
        return reverse(
            "finance:pricing_update", 
            kwargs={'slug': self.slug}
        )


def pre_save_pricing(sender, instance, *args, **kwargs):

    instance.slug = slugify(instance.pricing)
pre_save.connect(pre_save_pricing, sender=Pricing)


class Main(models.Model):
    main = "Parent Ledger"
        
    def __str__(self):
        return self.main

    def get_absolute_url(self):
        return reverse(
            "finance:main_detail", 
            kwargs={'pk': 1}
        )

    def get_customer_balance_sheet(self):
        """
        Creates a current customer balance number, including taxes separated 
        out.
        """
        total = 0
        taxes = 0
        balances = 0
        un_paid_count = 0
        conflicts = 0
        unresolved_conflicts = 0
        projected_before_tax = 0

        invoice_list = Customer_Invoice.objects.all()
        count = len(invoice_list)
        for invoice in invoice_list:
            if invoice.invoice_quote.total_price_quoted:
                total += invoice.invoice_quote.total_price_quoted
                taxes += invoice.invoice_quote.tax_on_quote
                balances += invoice.get_balance_due()
            else:
                projected = invoice.get_cost()
                projected_before_tax += projected[1]
            if not invoice.paid_in_full:
                un_paid_count += 1
            for conflict in invoice.conflict.all():
                conflicts += 1
                if not conflict.conflict_resolution:
                    unresolved_conflicts += 1
            profit = total - taxes

        return total, taxes, profit, balances, count, conflicts, unresolved_conflicts, projected_before_tax

    def get_operation_balance_sheet(self):
        """
        Creates a current operations balance number.
        """
        date_list = Operation_Invoice.objects.all().dates('origin', 'year')

        for years in date_list:
            Operation_Invoice.objects.filter(origin__year = years.year)

        expenses = 0
        balances = 0
        un_paid_count = 0
        conflicts = 0
        unresolved_conflicts = 0

        invoice_list = Operation_Invoice.objects.all()
        count = len(invoice_list)
        for invoice in invoice_list:
            expenses += invoice.invoice_amount
            balances += invoice.get_balance_due()
            if not invoice.paid_in_full:
                un_paid_count += 1
            for conflict in invoice.conflict.all():
                conflicts += 1
                if not conflict.conflict_resolution:
                    unresolved_conflicts += 1

        return expenses, balances, count, conflicts, unresolved_conflicts 
