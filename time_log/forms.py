from __future__ import unicode_literals

import re

from django import forms
# from employee.models import Employee
from django.forms import ModelForm, inlineformset_factory
from django.utils.translation import ugettext_lazy as _
from schedule.widgets import SpectrumColorPicker
from datetimewidget.widgets import TimeWidget

from .models import StaffLog


class StaffCreateForm(forms.ModelForm):
    pass

    # def __init__(self, *args, **kwargs):
    #     super(StaffCreateForm, self).__init__(*args, **kwargs)

    # class Meta:
    #     model = StaffLog
    #     fields = (
    #         "staff",
    #     )


class StaffAndTimeForm(forms.ModelForm):

    scheduled_start = forms.TimeField(
          widget=TimeWidget(bootstrap_version=3))

    scheduled_end = forms.TimeField(
          widget=TimeWidget(bootstrap_version=3))


class StaffLogCreateForm(StaffAndTimeForm):
    pass

#     def __init__(self, *args, **kwargs):
#         super(StaffLogCreateForm, self).__init__(*args, **kwargs)

#     class Meta:
#         model = StaffLog
#         fields = (
#             "staff", "day", "scheduled_start", "scheduled_end"
#         )

#     def clean(self):
#         cleaned_data = super(StaffLogCreateForm, self).clean()
#         if self.cleaned_data['scheduled_end'] <= self.cleaned_data['scheduled_start']:
#             raise forms.ValidationError(
#                 _(u"The end time must be later than start time.")
#             )
#         return self.cleaned_data


class StaffAndTimeFormSet(StaffLogCreateForm):
    pass
# = inlineformset_factory(

    # User, StaffLog,
#     form=StaffLogCreateForm, extra=1
# )
