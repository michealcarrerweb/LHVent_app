import re

from django import forms
from django.utils.translation import ugettext_lazy as _

only_letters = re.compile(r'^[a-z A-Z \']+$')
company_name_check = re.compile(r'^[a-z A-Z \' 0-9]+$')
check_phone = re.compile(r'^[0-9]{10}$')
check_mod_phone = re.compile(r'^\+1([0-9]{10})$')
check_mod_space_phone = re.compile(r'^([0-9]{3})( *)([0-9]{3})( *)([0-9]{4})$')


def check_name(name):
    """
    Handles ensuring entry uses only letter and is capitalized.
    """
    if not only_letters.search(name):
        raise forms.ValidationError(_('Enter a valid name. This \
                                      value must contain only letters.'))
    return name.capitalize()


def check_phone_options(value):
    if check_phone.search(value):
        value = "+1" + value
        return value
    elif check_mod_space_phone.search(value):
        value = "+1" + value
        return value
    elif check_mod_phone.search(value):               
        return value
    else:
        raise forms.ValidationError(_('Enter a valid phone number\
                                      - ex. 2223334444.')) 


# class CapitalizeForm(forms.ModelForm):

#     class Meta:
#         model = Invoice
#         fields = (
#             "total_price_quoted", "pricing", "tax", "note", 
#         )

#     def __init__(self, *args, **kwargs):
#         super(GiveQuoteForm, self).__init__(*args, **kwargs)
#         instance = getattr(self, 'instance', None)
#         if instance and instance.id:
#             self.fields['total_price_quoted'].widget.attrs['readonly'] = True