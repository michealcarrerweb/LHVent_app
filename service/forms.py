from __future__ import unicode_literals

from django import forms
# from django.forms.models import inlineformset_factory
from django.forms import ModelForm, inlineformset_factory
# from django.forms.formsets import BaseFormSet
import re
from .models import (Base, Service, PartsForService)
from source_utils.form_mixins import check_name


class BaseForm(forms.ModelForm):
    class Meta:
        model = Base
        fields = ('category',)
        
    def clean_category(self):
        """
        Handles validation.
        """
        return check_name(self.cleaned_data["category"])


class ServiceCreateForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = (
            "base", "service_description", "additional_hours", 
            "hourly_additional", "job_tools"
        )
        widgets = {'base': forms.HiddenInput(),
                    }


class ServiceUpdateForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = (
            "base", "service_description", "additional_hours", 
            "hourly_additional", "service_no_longer_available",
            "job_tools"
        )
        widgets = {'base': forms.HiddenInput(),
                    }


class PartsForServiceForm(forms.ModelForm):
    class Meta:
        model = PartsForService
        fields = ("service", "product", "quantity", "description")

PartsForServiceFormSet = inlineformset_factory(
    Service, PartsForService,
    form=PartsForServiceForm, extra=1
)
