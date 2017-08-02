from __future__ import unicode_literals

from django import forms
from django.forms import ModelForm, inlineformset_factory

from .models import Order


class ScheduledForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("scheduled",)
        widgets = {'scheduled': forms.HiddenInput(), }


class OrderPulledForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("pulled",)
        widgets = {'pulled': forms.HiddenInput(),}


class WorkInitiatedForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("work_initiated",)
        widgets = {'work_initiated': forms.HiddenInput(),}


class OrderCompletedForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("work_completed",)
        widgets = {'work_completed': forms.HiddenInput(),}


class ClosedForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ( "closed_out",)
        widgets = {'closed_out': forms.HiddenInput(),}
        

class PostponedForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("postponed",)
        widgets = {'postponed': forms.HiddenInput(),}


class DatesLoggedForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            "scheduled", 
            "pulled", 
            "work_initiated", 
            "work_completed", 
            "closed_out", 
            "postponed",
        )
        widgets = {
                   'scheduled': forms.HiddenInput(),
                   'pulled': forms.HiddenInput(),
                   'work_initiated': forms.HiddenInput(),
                   'work_completed': forms.HiddenInput(),
                   'closed_out': forms.HiddenInput(),
                   'postponed': forms.HiddenInput(),
        }