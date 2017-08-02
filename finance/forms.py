from __future__ import unicode_literals

from django import forms
import re
import string

from django.utils.translation import ugettext_lazy as _

from hourly.models import Hourly
from .models import Pricing
from source_utils.form_mixins import check_name


class PricingForm(forms.ModelForm):
    class Meta:
        model = Pricing
        fields = ('pricing', 'percentage',)
        
    def clean_pricing(self):
        """
        Handles validation.
        """
        return string.capwords(check_name(self.cleaned_data["pricing"]))


class HourlyBaseForm(forms.ModelForm):
    class Meta:
        model = Hourly
        fields = ('hourly_base',)
        