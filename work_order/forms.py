from __future__ import unicode_literals

from django import forms
from django.forms import ModelForm, inlineformset_factory

from .models import Order


class OrderPulledForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            "pulled",
        )
        widgets = {'pulled': forms.HiddenInput(),
                    }


class OrderCompletedForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            "work_completed",
        )
        widgets = {'work_completed': forms.HiddenInput(),
                    }