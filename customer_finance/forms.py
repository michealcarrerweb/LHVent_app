from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Invoice, CustomerConflict, InvoiceAlteration


class GiveQuoteForm(forms.ModelForm):

    class Meta:
        model = Invoice
        fields = (
            "pricing", "tax", "note", 
        )


class SettleForm(forms.ModelForm):

    class Meta:
        model = InvoiceAlteration
        fields = (
            "invoice", 
            "transaction_update", 
            "transaction_amount", 
            "transaction_note"
        )
        widgets = {'invoice': forms.HiddenInput(),
                    }


class ResolutionForm(forms.ModelForm):

    conflict_resolution = forms.CharField(
        required=True,
    )

    class Meta:
        model = CustomerConflict
        fields = (
            "conflict_description", "conflict_resolution", 
        )

    def __init__(self, *args, **kwargs):
        super(ResolutionForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            self.fields['conflict_description'].widget.attrs['readonly'] = True


class CloseOutForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = (
            "closed_out",
        )
        widgets = {'closed_out': forms.HiddenInput(),
                    }

    def clean(self):
        if not self.instance.paid_in_full or self.instance.over_paid or not \
            self.instance.work_order.closed_out or not self.instance.invoice_quote:
            raise forms.ValidationError(
                        _("This invoice cannot be closed out due to unfulfilled required activities.")
                    )
        conflict_count = self.instance.conflict.filter(conflict_resolution=None)                
        if conflict_count:
            if len(conflict_count) == 1:
                mesg_resp = "This invoice cannot be closed out due to a pending conflict."
            else:
                mesg_resp = "This invoice cannot be closed out due to {} pending conflicts.".format(
                    len(conflict_count)
                )
            raise forms.ValidationError(
                _(mesg_resp)
            )
