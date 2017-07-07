from __future__ import unicode_literals

from django import forms
import re
import string

from django.utils.translation import ugettext_lazy as _

from .models import Base, JobTool
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


class JobToolForm(forms.ModelForm):
    class Meta:
        model = JobTool
        fields = ("base", "supplier", "tool", "tool_type", "condition")

    def clean_tool(self):
        """
        Handles validation.
        """
        return string.capwords(self.cleaned_data["tool"])

