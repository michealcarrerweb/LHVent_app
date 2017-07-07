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

from operation_finance.models import Invoice as Operation_Invoice
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

    def __init__(self, *args, **kwargs):
        super(Main, self).__init__(*args, **kwargs)
        self.client_tot_invoiced = 0
        self.operation_tot_expenses = 0
        self.taxes_invoiced = 0
        self.client_balance = 0
        self.operation_balance = 0
        self.total_customer_inv_alterations = 0
        self.total_operation_inv_alterations = 0
        self.customer_conflicts = 0
        self.operational_conflict = 0
        
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
        customer_invoices = Customer_Invoice.objects.all()
        for customer in customer_invoices:
            if customer.invoice_quote.total_price_quoted:
                self.client_tot_invoiced += customer.invoice_quote.total_price_quoted
                self.taxes_invoiced += customer.invoice_quote.tax_on_quote
            customer.get_balance_due()
            self.total_customer_inv_alterations += customer.payments
            try:
                conflicts = CustomerConflict.objects.filter(invoice=customer)
                self.customer_conflicts += len(conflicts)
            except CustomerConflict.DoesNotExist:
                pass
        self.client_balance = self.total_customer_inv_alterations \
            - self.client_tot_invoiced

    def get_operation_balance_sheet(self):
        """
        Creates a current operations balance number.
        """
        operation_invoices = Operation_Invoice.objects.all()
        for operation in operation_invoices:
            self.operation_tot_expenses += operation.invoice_amount
            operation.get_balance()
            self.total_operation_inv_alterations += operation.payments
            if operation.conflict:
                self.operational_conflict += 1
        self.operation_balance = self.total_operation_inv_alterations \
            - self.operation_tot_expenses

    def get_balance_sheet(self):
        """
        Creates a current total balance number, including taxes separated 
        out.
        """
        self.get_customer_balance_sheet()
        self.get_operation_balance_sheet()
        return self.total_customer_inv_alterations \
            - self.total_operation_inv_alterations
        

    def get_projected_balance_sheet(self):
        """
        Creates a current total balance number, including taxes separated 
        out.
        """
        return self.client_tot_invoiced - self.operation_tot_expenses \
            - self.taxes_invoiced
