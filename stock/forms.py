from __future__ import unicode_literals

from django import forms
import re
import string

from django.utils.translation import ugettext_lazy as _

from .models import Base, Product
from company.models import Company
from source_utils.form_mixins import (
    check_name, 
    check_phone_options, 
    company_name_check
)


class BaseForm(forms.ModelForm):
    class Meta:
        model = Base
        fields = ('category',)
        
    def clean_category(self):
        """
        Handles validation.
        """
        return check_name(self.cleaned_data["category"])


class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            "base", "supplier", "item", "quantity", "admin_time", "prep_time", 
            "field_time", "admin_material", "prep_material", "field_material", 
            "quantity_assesement", "order_if_below", "order_now", 
            "units_damaged_or_lost", "image"
        )


    def clean_item(self):
        """
        Handles validation.
        """
        return string.capwords(self.cleaned_data["item"])


class ProductUpdateForm(ProductCreateForm):
    pass
 

class ImageUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ("image",)  


class ItemAddDamagedForm(forms.Form):
    damaged_or_lost = forms.IntegerField(label='Quantity of damaged or lost?')


class ItemAddedForm(forms.Form):
    added = forms.IntegerField(label='Add additional to stock?')