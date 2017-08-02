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
            "vendor", "plu", "invoice_amount", "due_by", "note", "file",
            "image",
        )


class InvoiceUpdateForm(InvoiceForm):

    pass
             