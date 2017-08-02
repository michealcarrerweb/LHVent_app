from __future__ import unicode_literals

from decimal import Decimal

from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Invoice, InvoiceAlteration, VendorConflict 
from .forms import InvoiceForm, InvoiceUpdateForm
from customer_finance.forms import GiveQuoteForm, ResolutionForm, SettleForm
from source_utils.permission_mixins import FinanceCheckMixin, SuperUserCheckMixin
from source_utils.view_mixins import DeleteViewMixin


class InvoiceMixin(FinanceCheckMixin):
    model = Invoice


class InvoicesOptionsListView(InvoiceMixin, ListView):
    # success_url = reverse_lazy('operation_finance:invoice_lists')
    template_name = "operation_finance/optional_lists.html"
    paginate_by = 10

    def get_queryset(self):
        if self.args[0] == "owed":
            return Invoice.objects.filter(paid_in_full=False)
        elif self.args[0] == "conflicted":
            self.template_name = "operation_finance/conflict_list.html"
            return VendorConflict.objects.filter(conflict_resolution=None)
        elif self.args[0] == "active":
            return Invoice.objects.filter(paid_in_full=False)
        else:
            return Invoice.objects.all()

    def get_context_data(self, **kwargs):
        context = super(InvoicesOptionsListView, self).get_context_data(**kwargs)
        if self.args[0] == "owed":
            context['title'] = "Invoices with Balances"
        elif self.args[0] == "conflicted":
            context['title'] = "Invoices with Conflicts"
        elif self.args[0] == "active":
            context['title'] = "Active Invoices"
        else:
            context['title'] = "All Invoices"
        return context


class InvoiceDetailView(InvoiceMixin, DetailView):
    template_name = "operation_finance/invoice_detail.html"
    url_insert = "operation_finance:invoice_delete"

    def get_context_data(self, **kwargs):
        context = super(InvoiceDetailView, self).get_context_data(**kwargs)
        context['balance_due'] = self.object.get_balance_due()
        context['payment_schedule'] = self.object.get_payment_schedule()

        return context


class InvoiceEditMixin(InvoiceMixin, SuccessMessageMixin):
    template_name = 'form.html'
    form_class = InvoiceForm

    def __init__(self, *args, **kwargs):
        super(InvoiceEditMixin, self).__init__(*args, **kwargs)
        self.name = "invoice"

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            item=self.object.vendor,
            action=self.action
        )


class InvoicesOwedView(InvoiceMixin, ListView):
    template_name = "operation_finance/invoice_list.html"

    def get_queryset(self):
        return Invoice.objects.filter(paid_in_full=False)

    def get_context_data(self, **kwargs):
        context = super(InvoicesOwedView, self).get_context_data(**kwargs)
        context['title'] = "Operation Invoices with Balances"
        return context


class InvoicesConflictView(InvoicesOwedView):
    template_name = "operation_finance/invoice_list.html"

    def get_queryset(self):
        return Invoice.objects.filter(conflict=True)

    def get_context_data(self, **kwargs):
        context = super(InvoicesConflictView, self).get_context_data(**kwargs)
        context['title'] = "Operation Invoices with Conflicts"
        return context


class InvoiceCreateView(InvoiceEditMixin, CreateView):
    success_message = "%(item)s was successfully created"
    title = "New Invoice"

    def __init__(self, *args, **kwargs):
        super(InvoiceCreateView, self).__init__(*args, **kwargs)
        self.action = "add"


class InvoiceUpdateView(InvoiceEditMixin, UpdateView):
    success_message = "%(item)s was successfully updated"
    title = "Update Invoice"
    form_class = InvoiceUpdateForm

    def __init__(self, *args, **kwargs):
        super(InvoiceUpdateView, self).__init__(*args, **kwargs)
        self.action = "edit"


class InvoiceDeleteView(DeleteViewMixin):
    model = Invoice
    success_url = reverse_lazy('operation_finance:invoice_lists', args=['active'])


class AlterationMixin(FinanceCheckMixin):
    model = InvoiceAlteration


class AlterationByInvoiceListView(AlterationMixin, ListView):
    template_name = "operation_finance/alteration_list.html"

    def get_queryset(self):
        self.invoice_list = get_object_or_404(Invoice, slug=self.args[0])
        return InvoiceAlteration.objects.filter(invoice=self.invoice_list)


class AlterationDetailView(AlterationMixin, DetailView):
    template_name = "operation_finance/alteration_detail.html"


class AlterationEditMixin(AlterationMixin, SuccessMessageMixin):
    template_name = 'form.html'
    fields = ["invoice", "transaction_update", "transaction_amount", 
              "transaction_note"]

    def __init__(self, *args, **kwargs):
        super(AlterationEditMixin, self).__init__(*args, **kwargs)
        self.name = "alteration"

    def get_success_message(self, cleaned_data):
        invoice_name = "{} {}".format(
            self.object.invoice.vendor, 
            self.object.invoice.origin
        )
        return self.success_message % dict(
            cleaned_data,
            item="$" + str(self.object.transaction_amount),
            action=self.action,
            location="to " + invoice_name,
        )


class AlterationCreateView(AlterationEditMixin, CreateView):

    def __init__(self, *args, **kwargs):
        super(AlterationCreateView, self).__init__(*args, **kwargs)
        self.action = "add"

    def get_initial(self):
        invoice = get_object_or_404(Invoice, slug=self.kwargs.get('slug'))
        return_balance = invoice.get_balance_due()
        self.balance = return_balance
        return {
        'invoice':invoice,
        }

    def get_context_data(self, **kwargs):
        context = super(
            AlterationCreateView, self).get_context_data(**kwargs
        )
        context['title'] = "Settle invoice"
        context['balance'] = self.balance
        return context


class ConflictMixin(FinanceCheckMixin):
    model = VendorConflict


class VendorConflictMixin(ConflictMixin, SuccessMessageMixin):
    success_message = "Conflict was successfully %(action)s invoice %(location)s"
    template_name = 'form.html'
    action = "added to"

    def get_success_url(self):
        return reverse('operation_finance:invoice_lists', args=["conflicted"])

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            action=self.action,
            location=self.object.invoice
        )


class VendorConflictCreateView(VendorConflictMixin, CreateView):
    fields = ["invoice", "conflict_description"]

    def get_initial(self):
        self.invoice = get_object_or_404(Invoice, slug=self.kwargs.get('slug'))
        return {
            'invoice':self.invoice,
        }

    def get_context_data(self, **kwargs):
        context = super(VendorConflictCreateView, self).get_context_data(**kwargs)
        context['title'] = "New Conflict for {}".format(self.invoice)
        return context


class VencorConflictUpdateView(VendorConflictMixin, UpdateView):
    fields = ["conflict_description"]

    def get_context_data(self, **kwargs):
        context = super(VencorConflictUpdateView, self).get_context_data(**kwargs)
        context['title'] = "Update Conflict for {}".format(self.object.invoice)
        return context


class VendorConflictResolveView(VendorConflictMixin, UpdateView):
    form_class = ResolutionForm
    action = "resolved for"

    def get_context_data(self, **kwargs):
        context = super(VendorConflictResolveView, self).get_context_data(**kwargs)
        context['title'] = "Resolve Conflict for {}".format(self.object.invoice)
        return context
