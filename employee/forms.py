from __future__ import unicode_literals

import re
import string

try:
    from collections import OrderedDict
except ImportError:
    OrderedDict = None

from django import forms
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from account.conf import settings
from account.hooks import hookset
from account.models import EmailAddress
from account.utils import get_user_lookup_kwargs
from account.states import state_choices



# alnum_re = re.compile(r"^\w+$")
alnum_re = re.compile(r'^[\w.@+-]+$')#re.compile(r"^\w+$")
    #changed to meet username requirements
check_names = re.compile(r'^[\w]+$')
check_phone = re.compile(r'^[0-9]{10}$')
check_mod_phone = re.compile(r'^\+1([0-9]{10})$')
check_mod_space_phone = re.compile(r'^([0-9]{3})( *)([0-9]{3})( *)([0-9]{4})$')
check_zip = re.compile(r'^[0-9]{5}$')


class Clean_Checks(object):

    def check_phone_options(self, value):
        if check_phone.search(value):
            value = "+1" + value
            return value
        elif check_mod_space_phone.search(value):
            value = "+1" + value
            return value
        elif check_mod_phone.search(value):               
            return value
        else:
            raise forms.ValidationError(_('Enter a valid phone number - ex. 2223334444.')) 

    def clean_username(self):
        if not alnum_re.search(self.cleaned_data["username"]):
            raise forms.ValidationError(_('Enter a valid username. This value may contain only letters, '
                                            'numbers, and @/./+/-/_ characters.'))
        User = get_user_model()
        lookup_kwargs = get_user_lookup_kwargs({
            "{username}__iexact": self.cleaned_data["username"]
        })
        qs = User.objects.filter(**lookup_kwargs)
        if not qs.exists():
            return self.cleaned_data["username"]
        raise forms.ValidationError(_("This username is already taken. Please choose another."))

    def clean_email(self):
        value = self.cleaned_data["email"]
        qs = EmailAddress.objects.filter(email__iexact=value)
        if not qs.exists() or not settings.ACCOUNT_EMAIL_UNIQUE:
            return value
        raise forms.ValidationError(_("A user is registered with this email address."))

    def clean_first_name(self):
        if not check_names.search(self.cleaned_data["first_name"]):
            raise forms.ValidationError(_('Enter a valid first name. This value must contain only letters.'))
        value = self.cleaned_data["first_name"]
        return value.capitalize()

    def clean_spouse_name(self):
        if self.cleaned_data["spouse_name"]:
            if not check_names.search(self.cleaned_data["spouse_name"]):
                raise forms.ValidationError(_('Enter a valid first name. This value must contain only letters.'))
            value = self.cleaned_data["spouse_name"]
            return value.capitalize()
        else:
            return None

    def clean_last_name(self):
        if not check_names.search(self.cleaned_data["last_name"]):
            raise forms.ValidationError(_('Enter a valid first name. This value must contain only letters.'))
        value = self.cleaned_data["last_name"]
        return value.capitalize()

    def clean_street_address(self):
        value = self.cleaned_data["street_address"]
        return string.capwords(value)

    def clean_city(self):
        value = self.cleaned_data["city"]
        return value.capitalize()

    def clean_main_phone(self):
        value = self.cleaned_data["main_phone"]
        return self.check_phone_options(value)

    def clean_alt_phone(self):
        value = self.cleaned_data["alt_phone"]
        if value == "":
            return None
        return self.check_phone_options(value)

    def clean_zip_code(self):
        if not check_zip.search(self.cleaned_data["zip_code"]):
            raise forms.ValidationError(_('Enter a valid zip code. This value must contain exactly 5 numbers.'))
        return self.cleaned_data["zip_code"]


class BasicAddress(Clean_Checks, forms.Form):

    STATE_CHOICES = state_choices

    username = forms.CharField(
        label=_("Username - email suggested"),
        max_length=30,
        widget=forms.TextInput(),
        required=True
    )
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.TextInput(), required=True
    )
    first_name = forms.CharField(
        label=_("Name"),
        max_length=30,
        widget=forms.TextInput(),
        required=False
    )
    spouse_name = forms.CharField(
        label=_("Spouses' name - not required"),
        max_length=30,
        widget=forms.TextInput(),
        required=False
    )
    last_name = forms.CharField(
        label=_("Last name"),
        max_length=30, 
        widget=forms.TextInput(),
        required=True
    )
    street_address = forms.CharField(
        label=_("Street address"),
        max_length=30, 
        widget=forms.TextInput(),
        required=True
    )
    city = forms.CharField(
        label=_("City"),
        max_length=30, 
        widget=forms.TextInput(),
        required=True
    )
    state = forms.ChoiceField(
        label=_("State"),
        widget=forms.Select(),
        choices=STATE_CHOICES,
        # initial='PA',
        required=True
    )
    zip_code = forms.CharField(
        label=_("Zip code - ex. '18951'"), 
        widget=forms.TextInput(),
        required=True
    )
    main_phone = forms.CharField(
        label=_("Phone"),
        widget=forms.TextInput(),
        required=True
    )
    alt_phone = forms.CharField(
        label=_("Alternate phone - not required"), 
        widget=forms.TextInput(),
        required=False
    )

    # def check_phone_options(self, value):
    #     if check_phone.search(value):
    #         value = "+1" + value
    #         return value
    #     elif check_mod_space_phone.search(value):
    #         value = "+1" + value
    #         return value
    #     elif check_mod_phone.search(value):               
    #         return value
    #     else:
    #         raise forms.ValidationError(_('Enter a valid phone number - ex. 2223334444.')) 

    # def clean_username(self):
    #     if not alnum_re.search(self.cleaned_data["username"]):
    #         raise forms.ValidationError(_('Enter a valid username. This value may contain only letters, '
    #                                         'numbers, and @/./+/-/_ characters.'))
    #     User = get_user_model()
    #     lookup_kwargs = get_user_lookup_kwargs({
    #         "{username}__iexact": self.cleaned_data["username"]
    #     })
    #     qs = User.objects.filter(**lookup_kwargs)
    #     if not qs.exists():
    #         return self.cleaned_data["username"]
    #     raise forms.ValidationError(_("This username is already taken. Please choose another."))

    # def clean_email(self):
    #     value = self.cleaned_data["email"]
    #     qs = EmailAddress.objects.filter(email__iexact=value)
    #     if not qs.exists() or not settings.ACCOUNT_EMAIL_UNIQUE:
    #         return value
    #     raise forms.ValidationError(_("A user is registered with this email address."))

    # def clean_first_name(self):
    #     if not check_names.search(self.cleaned_data["first_name"]):
    #         raise forms.ValidationError(_('Enter a valid first name. This value must contain only letters.'))
    #     value = self.cleaned_data["first_name"]
    #     return value.capitalize()

    # def clean_spouse_name(self):
    #     if self.cleaned_data["spouse_name"]:
    #         if not check_names.search(self.cleaned_data["spouse_name"]):
    #             raise forms.ValidationError(_('Enter a valid first name. This value must contain only letters.'))
    #         value = self.cleaned_data["spouse_name"]
    #         return value.capitalize()
    #     else:
    #         return None

    # def clean_last_name(self):
    #     if not check_names.search(self.cleaned_data["last_name"]):
    #         raise forms.ValidationError(_('Enter a valid first name. This value must contain only letters.'))
    #     value = self.cleaned_data["last_name"]
    #     return value.capitalize()

    # def clean_street_address(self):
    #     value = self.cleaned_data["street_address"]
    #     return string.capwords(value)

    # def clean_city(self):
    #     value = self.cleaned_data["city"]
    #     return value.capitalize()

    # def clean_main_phone(self):
    #     value = self.cleaned_data["main_phone"]
    #     return self.check_phone_options(value)

    # def clean_alt_phone(self):
    #     value = self.cleaned_data["alt_phone"]
    #     if value == "":
    #         return None
    #     return self.check_phone_options(value)

    # def clean_zip_code(self):
    #     if not check_zip.search(self.cleaned_data["zip_code"]):
    #         raise forms.ValidationError(_('Enter a valid zip code. This value must contain exactly 5 numbers.'))
    #     return self.cleaned_data["zip_code"]


class PasswordField(forms.CharField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", forms.PasswordInput(render_value=False))
        self.strip = kwargs.pop("strip", True)
        super(PasswordField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if value in self.empty_values:
            return ""
        value = force_text(value)
        if self.strip:
            value = value.strip()
        return value


class SignupForm(BasicAddress):

    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(render_value=False)
    )
    password_confirm = forms.CharField(
        label=_("Password (again)"),
        widget=forms.PasswordInput(render_value=False)
    )
    code = forms.CharField(
        max_length=64,
        required=False,
        widget=forms.HiddenInput()
    )

    def clean(self):
        if "password" in self.cleaned_data and "password_confirm" in self.cleaned_data:
            if self.cleaned_data["password"] != self.cleaned_data["password_confirm"]:
                raise forms.ValidationError(_("You must type the same password each time."))
        return self.cleaned_data
#########################

class StaffSignupForm(Clean_Checks, forms.ModelForm):

    class Meta:
        model = User
        fields = [
                'username', 'email', 'first_name', 'spouse_name', 
                  'last_name', 'street_address', 'city', 'zip_code', 
                  'main_phone', 'is_warehouse', 'is_service', 
                  'is_maintenance', 'is_manager'
        ]

    main_phone = forms.CharField(
        label=_("Phone"),
        widget=forms.TextInput(),
        required=True
    )


class ClientSignupForm(Clean_Checks, forms.ModelForm):

    class Meta:
        model = User
        fields = [
                'username', 'email', 'first_name', 'spouse_name', 
                  'last_name', 'street_address', 'city', 'zip_code', 
                  'main_phone'
        ]

    main_phone = forms.CharField(
        label=_("Phone"),
        widget=forms.TextInput(),
        required=True
    )


class StaffUpdateForm(StaffSignupForm):

    def clean_username(self):
        value = self.cleaned_data["username"]
        if self.initial.get("username") == value:
            return value
        if not alnum_re.search(value):
            raise forms.ValidationError(_('Enter a valid username. This value may contain only letters, '
                                            'numbers, and @/./+/-/_ characters.'))
        User = get_user_model()
        lookup_kwargs = get_user_lookup_kwargs({
            "{username}__iexact": self.cleaned_data["username"]
        })
        qs = User.objects.filter(**lookup_kwargs)
        if not qs.exists():
            return self.cleaned_data["username"]
        raise forms.ValidationError(_("This username is already taken. Please choose another."))

    def clean_email(self):
        value = self.cleaned_data["email"]
        if self.initial.get("email") == value:
            return value
        qs = EmailAddress.objects.filter(email__iexact=value)
        if not qs.exists() or not settings.ACCOUNT_EMAIL_UNIQUE:
            return value
        raise forms.ValidationError(_("A user is registered with this email address."))


class StaffUpdateToSuperFinanceForm(StaffUpdateForm):

    class Meta:
        model = User
        fields = [
                'username', 'email', 'first_name', 'spouse_name', 
                  'last_name', 'street_address', 'city', 'zip_code', 
                  'main_phone', 'is_warehouse', 'is_service', 
                  'is_maintenance', 'is_manager', 'is_financial', 
                  'is_superuser'
        ]


class LoginForm(forms.Form):

    password = PasswordField(
        label=_("Password"),
        strip=settings.ACCOUNT_PASSWORD_STRIP,
    )
    remember = forms.BooleanField(
        label=_("Remember Me"),
        required=False
    )
    user = None

    def clean(self):
        if self._errors:
            return
        user = auth.authenticate(**self.user_credentials())
        if user:
            if user.is_active:
                self.user = user
            else:
                raise forms.ValidationError(_("This account is inactive."))
        else:
            raise forms.ValidationError(self.authentication_fail_message)
        return self.cleaned_data

    def user_credentials(self):
        return hookset.get_user_credentials(self, self.identifier_field)


class LoginUsernameForm(LoginForm):

    username = forms.CharField(label=_("Username"), max_length=30)
    authentication_fail_message = _("The username and/or password you specified are not correct.")
    identifier_field = "username"

    def __init__(self, *args, **kwargs):
        super(LoginUsernameForm, self).__init__(*args, **kwargs)
        field_order = ["username", "password", "remember"]
        if not OrderedDict or hasattr(self.fields, "keyOrder"):
            self.fields.keyOrder = field_order
        else:
            self.fields = OrderedDict((k, self.fields[k]) for k in field_order)


class LoginEmailForm(LoginForm):

    email = forms.EmailField(label=_("Email"))
    authentication_fail_message = _("The email address and/or password you specified are not correct.")
    identifier_field = "email"

    def __init__(self, *args, **kwargs):
        super(LoginEmailForm, self).__init__(*args, **kwargs)
        field_order = ["email", "password", "remember"]
        if not OrderedDict or hasattr(self.fields, "keyOrder"):
            self.fields.keyOrder = field_order
        else:
            self.fields = OrderedDict((k, self.fields[k]) for k in field_order)


class ChangePasswordForm(forms.Form):

    password_current = forms.CharField(
        label=_("Current Password"),
        widget=forms.PasswordInput(render_value=False)
    )
    password_new = forms.CharField(
        label=_("New Password"),
        widget=forms.PasswordInput(render_value=False)
    )
    password_new_confirm = forms.CharField(
        label=_("New Password (again)"),
        widget=forms.PasswordInput(render_value=False)
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean_password_current(self):
        if not self.user.check_password(self.cleaned_data.get("password_current")):
            raise forms.ValidationError(_("Please type your current password."))
        return self.cleaned_data["password_current"]

    def clean_password_new_confirm(self):
        if "password_new" in self.cleaned_data and "password_new_confirm" in self.cleaned_data:
            if self.cleaned_data["password_new"] != self.cleaned_data["password_new_confirm"]:
                raise forms.ValidationError(_("You must type the same password each time."))
        return self.cleaned_data["password_new_confirm"]


class PasswordResetForm(forms.Form):

    email = forms.EmailField(label=_("Email"), required=True)

    def clean_email(self):
        value = self.cleaned_data["email"]
        if not EmailAddress.objects.filter(email__iexact=value).exists():
            raise forms.ValidationError(_("Email address can not be found."))
        return value


class PasswordResetTokenForm(forms.Form):

    password = forms.CharField(
        label=_("New Password"),
        widget=forms.PasswordInput(render_value=False)
    )
    password_confirm = forms.CharField(
        label=_("New Password (again)"),
        widget=forms.PasswordInput(render_value=False)
    )

    def clean_password_confirm(self):
        if "password" in self.cleaned_data and "password_confirm" in self.cleaned_data:
            if self.cleaned_data["password"] != self.cleaned_data["password_confirm"]:
                raise forms.ValidationError(_("You must type the same password each time."))
        return self.cleaned_data["password_confirm"]


class SettingsForm(BasicAddress):

    def clean_username(self):
        value = self.cleaned_data["username"]
        if self.initial.get("username") == value:
            return value
        if not alnum_re.search(value):
            raise forms.ValidationError(_('Enter a valid username. This value may contain only letters, '
                                            'numbers, and @/./+/-/_ characters.'))
        User = get_user_model()
        lookup_kwargs = get_user_lookup_kwargs({
            "{username}__iexact": self.cleaned_data["username"]
        })
        qs = User.objects.filter(**lookup_kwargs)
        if not qs.exists():
            return self.cleaned_data["username"]
        raise forms.ValidationError(_("This username is already taken. Please choose another."))

    def clean_email(self):
        value = self.cleaned_data["email"]
        if self.initial.get("email") == value:
            return value
        qs = EmailAddress.objects.filter(email__iexact=value)
        if not qs.exists() or not settings.ACCOUNT_EMAIL_UNIQUE:
            return value
        raise forms.ValidationError(_("A user is registered with this email address."))
    
    def clean_first_name(self):
        value = self.cleaned_data["first_name"]
        if self.initial.get("first_name") == value:
            return value.capitalize()
        if not check_names.search(value):
            raise forms.ValidationError(_('Enter a valid first name. This value must contain only letters.'))
        return value.capitalize()

    def clean_spouse_name(self):
        new_value = self.cleaned_data["spouse_name"]
        old_value = self.initial.get("spouse_name")
        if new_value == old_value:
            return old_value.capitalize()
        if new_value == "":
            return None
        else:
            if not check_names.search(new_value):
                raise forms.ValidationError(_('Enter a valid name. This value must contain only letters.'))
            return new_value.capitalize()

    def clean_last_name(self):
        value = self.cleaned_data["last_name"]
        if self.initial.get("last_name") == value:
            return value.capitalize()
        if not check_names.search(value):
            raise forms.ValidationError(_('Enter a valid first name. This value must contain only letters.'))
        return value.capitalize()

    def clean_street_address(self):
        value = self.cleaned_data["street_address"]
        if self.initial.get("street_address") == value:
            return value
        return string.capwords(value)

    def clean_city(self):
        value = self.cleaned_data["city"]
        if self.initial.get("city") == value:
            return value
        return string.capwords(value)

    def clean_main_phone(self):
        value = self.cleaned_data["main_phone"]
        if self.initial.get("main_phone") == value:
            return value
        return self.check_phone_options(value)

    def clean_alt_phone(self):
        value = self.cleaned_data["alt_phone"]
        old_value = self.initial.get("alt_phone")
        if value == old_value:
            return old_value
        if value == "":
            return None
        return self.check_phone_options(value)
                
    def clean_zip_code(self):
        value = self.cleaned_data["zip_code"]
        if self.initial.get("zip_code") == value:
            return value
        if not check_zip.search(value):
            raise forms.ValidationError(_('Enter a valid zip code. This value must contain exactly 5 numbers.'))
        return value
