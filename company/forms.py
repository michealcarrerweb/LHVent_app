from __future__ import unicode_literals

from django import forms
import re
import string

from django.utils.translation import ugettext_lazy as _

from company.models import Company
from source_utils.form_mixins import (
    check_phone_options, 
    company_name_check
)


class CompanyCreateForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = (
            "company", "address", "company_phone"
        )

    def clean_company(self):
        """
        Handles validation.
        """
        name = self.cleaned_data["company"]
        if not company_name_check.search(name):
            raise forms.ValidationError(
                _('Enter a valid name. This value must contain only letters, \
                numbers and \'.')
            )
        return string.capwords(name)

    def clean_address(self):
        """
        Handles validation.
        """
        return string.capwords(self.cleaned_data["address"])

    def clean_company_phone(self):
        value = self.cleaned_data["company_phone"]
        if value == "":
            return None
        return check_phone_options(value)


class CompanyUpdateForm(CompanyCreateForm):
    class Meta:
        model = Company
        fields = (
            "company", "address", "company_phone", "no_longer_use"
        )