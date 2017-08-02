from __future__ import unicode_literals

import re
import time

from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm, inlineformset_factory
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from schedule.widgets import SpectrumColorPicker
from datetimewidget.widgets import TimeWidget
from source_utils.form_mixins import check_time_input

from .models import AvailabilityForDay, DAYS_OF_WEEK


class StaffAddToBaseForm(forms.ModelForm):
    scheduled_start = forms.TimeField(widget=forms.TimeInput(format='%H:%M'), initial="7:00")
    scheduled_end = forms.TimeField(widget=forms.TimeInput(format='%H:%M'), initial="17:00")

    class Meta:
        model = AvailabilityForDay
        fields = (
            "staff", "day", "scheduled_start", "scheduled_end"
        )

    def clean(self):
        cleaned_data = super(StaffAddToBaseForm, self).clean()
        time_format = 'Enter a valid time using a valid 24 hour format (example: "7:00" or "14:00" ).'
        if not check_time_input.search(str(self.cleaned_data.get('scheduled_start'))):
            raise forms.ValidationError(
        		_(time_format)
        	)
        if not check_time_input.search(str(self.cleaned_data.get('scheduled_end'))):
            raise forms.ValidationError(
        		_(time_format)
        	)
        elif self.cleaned_data['scheduled_end'] <= self.cleaned_data['scheduled_start']:
            raise forms.ValidationError(
                _(u"The end time must be later than start time.")
            )
        return self.cleaned_data


class StaffCreateForm(StaffAddToBaseForm):
    day = forms.ChoiceField(choices=DAYS_OF_WEEK)

    class Meta:
        model = AvailabilityForDay
        fields = (
            "staff", "day", "scheduled_start", "scheduled_end"
        )

    def __init__(self, *args, **kwargs):
        super(StaffCreateForm, self).__init__(*args, **kwargs)
        staff_queryset = AvailabilityForDay.objects.order_by('staff').distinct('staff')
        self.fields['staff'].queryset = User.objects.filter(is_staff=True).exclude(employee__in=staff_queryset)

    def clean(self):
        cleaned_data = super(StaffCreateForm, self).clean()
        time_format = 'Enter a valid time using a valid 24 hour format (example: "7:00" or "14:00" ).'
        if not check_time_input.search(str(self.cleaned_data.get('scheduled_start'))):
            raise forms.ValidationError(
        		_(time_format)
        	)
        if not check_time_input.search(str(self.cleaned_data.get('scheduled_end'))):
            raise forms.ValidationError(
        		_(time_format)
        	)
        elif self.cleaned_data['scheduled_end'] <= self.cleaned_data['scheduled_start']:
            raise forms.ValidationError(
                _(u"The end time must be later than start time.")
            )
        return self.cleaned_data


class StaffAddToForm(StaffAddToBaseForm):

    def __init__(self, days_of_week, *args, **kwargs):
        super(StaffAddToForm, self).__init__(*args, **kwargs)
        self.fields['day'] = forms.ChoiceField(
            days_of_week
        )

    class Meta:
        model = AvailabilityForDay
        fields = (
            "staff", "day", "scheduled_start", "scheduled_end"
        )
        widgets = {'staff': forms.HiddenInput(),}


class StaffLogUpdateForm(StaffAddToBaseForm):

    class Meta:
        model = AvailabilityForDay
        fields = (
            "scheduled_start", "scheduled_end"
        )




# class StaffAndTimeFormSet(StaffLogCreateForm):
#     pass
# # = inlineformset_factory(

#     # User, StaffLog,
# #     form=StaffLogCreateForm, extra=1
# # )
