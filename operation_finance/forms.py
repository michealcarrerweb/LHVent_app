from __future__ import unicode_literals

from django import forms
import re
import string

from django.utils.translation import ugettext_lazy as _

from .models import Invoice
from source_utils.form_mixins import check_name


class InvoiceForm(forms.ModelForm):

    class Meta:
        model = Invoice
        fields = (
            "invoice", "plu", "invoice_amount", "due_by", "note",
            "image",
        )
        
    def clean_invoice(self):
        """
        Handles validation.
        """
        return string.capwords(check_name(self.cleaned_data["invoice"]))


class InvoiceUpdateForm(forms.ModelForm):

    class Meta:
        model = Invoice
        fields = (
            "invoice", "plu", "invoice_amount", "due_by", "note",
            "conflict", "conflict_description", "image", 
        )
        
    def clean_invoice(self):
        """
        Handles validation.
        """
        return string.capwords(check_name(self.cleaned_data["invoice"]))
# class PricingForm(forms.ModelForm):
#     class Meta:
#         model = Pricing
#         fields = ('pricing', 'percentage',)
        
#     def clean_pricing(self):
#         """
#         Handles validation.
#         """
#         return string.capwords(check_name(self.cleaned_data["pricing"]))


# class HourlyBaseForm(forms.ModelForm):
#     class Meta:
#         model = Hourly
#         fields = ('hourly_base',)
#         