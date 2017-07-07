from __future__ import unicode_literals

from django import forms

from .models import Invoice, CustomerConflict, InvoiceAlteration


class GiveQuoteForm(forms.ModelForm):

    class Meta:
        model = Invoice
        fields = (
            "pricing", "tax", "note", 
        )

    # def __init__(self, *args, **kwargs):
    #     super(GiveQuoteForm, self).__init__(*args, **kwargs)
    #     instance = getattr(self, 'instance', None)
    #     if instance and instance.id:
    #         self.fields['total_price_quoted'].widget.attrs['readonly'] = True


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

    # def __init__(self, *args, **args):
    #     super(SettleForm, self).__init__(*args, **kwargs)
    #     # instance = getattr(self, 'instance', None)
    #     # if instance and instance.id:
    #     self.fields['invoice'].widget.atkwargs):
    #     super(SettleForm, self).__init__(*args, **kwargs)
    #     # instance = getattr(self, 'instance', None)
    #     # if instance and instance.id:
    #     self.fields['invoice'].widget.attrs['readonly'] = True


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
