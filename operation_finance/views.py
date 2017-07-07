from __future__ import unicode_literals

from decimal import Decimal

from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# from finance.models import Ledger
from .models import Invoice, InvoiceAlteration
from .forms import InvoiceForm, InvoiceUpdateForm
from source_utils.permission_mixins import FinanceCheckMixin, SuperUserCheckMixin
from source_utils.view_mixins import DeleteViewMixin, ContextMixin

#2
class InvoiceMixin(FinanceCheckMixin):
    model = Invoice


class InvoiceDetailView(InvoiceMixin, DetailView):
    template_name = "operation_finance/invoice_detail.html"


class InvoiceListView(InvoiceMixin, ContextMixin, ListView):

    def __init__(self, *args, **kwargs):
    	super(InvoiceListView, self).__init__(*args, **kwargs)
    	self.name = "invoice"
    	self.action = "categories"


class InvoiceEditMixin(InvoiceMixin, ContextMixin, SuccessMessageMixin):
    template_name = 'form.html'
    form_class = InvoiceForm

    def __init__(self, *args, **kwargs):
    	super(InvoiceEditMixin, self).__init__(*args, **kwargs)
    	self.name = "invoice"

    def get_success_message(self, cleaned_data):
    	return self.success_message % dict(
    		cleaned_data,
    		item=self.object.invoice,
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

    def __init__(self, *args, **kwargs):
    	super(InvoiceCreateView, self).__init__(*args, **kwargs)
    	self.action = "add"


class InvoiceUpdateView(InvoiceEditMixin, UpdateView):
    form_class = InvoiceUpdateForm

    def __init__(self, *args, **kwargs):
    	super(InvoiceUpdateView, self).__init__(*args, **kwargs)
    	self.action = "edit"


class InvoiceDeleteView(DeleteViewMixin):
	model = Invoice
	success_url = reverse_lazy('operation_finance:invoice_list')


class AlterationMixin(FinanceCheckMixin):
	model = InvoiceAlteration


class AlterationDetailView(AlterationMixin, DetailView):
	template_name = "operation_finance/alteration_detail.html"


class AlterationEditMixin(AlterationMixin, ContextMixin, SuccessMessageMixin):
	template_name = 'form.html'
	fields = ["invoice", "transaction_update", "transaction_amount", 
			  "transaction_note"]

	def __init__(self, *args, **kwargs):
		super(AlterationEditMixin, self).__init__(*args, **kwargs)
		self.name = "alteration"

	def get_success_message(self, cleaned_data):
		invoice_name = "{} {}".format(
			self.object.invoice.invoice, 
			self.object.invoice.origin
		)
		return self.success_message % dict(
			cleaned_data,
			item="$" + str(self.object.transaction_amount),
			action=self.action,
			location="to " + invoice_name,
		)


class AlterationByInvoiceListView(AlterationMixin, ListView):
	template_name = "operation_finance/alteration_list.html"

	def get_queryset(self):
		self.invoice_list = get_object_or_404(Invoice, slug=self.args[0])
		return InvoiceAlteration.objects.filter(invoice=self.invoice_list)

	def get_context_data(self, **kwargs):
		context = super(
			AlterationByInvoiceListView, self).get_context_data(**kwargs
		)
		context['title'] = "Alteration by Invoice"
		# context['ledger_list'] = self.ledger_list
		return context


class AlterationCreateView(AlterationEditMixin, CreateView):

	def __init__(self, *args, **kwargs):
		super(AlterationCreateView, self).__init__(*args, **kwargs)
		self.action = "add"

	def get_initial(self):
		invoice = get_object_or_404(Invoice, slug=self.kwargs.get('slug'))
		return_balance = invoice.get_balance()
		self.balance = invoice.balance
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


# def get_initial(self):
# 		invoice = get_object_or_404(Invoice, slug=self.kwargs.get('slug'))
# 		quote = invoice.get_cost()
# 		balance = invoice.get_balance_due()
# 		if invoice.balance_due == 0:
# 			self.balance = invoice.total_price_quoted
# 		else:
# 			self.balance = invoice.balance_due
# 		return {
# 		'invoice':invoice,
# 		}

# 	def get_context_data(self, **kwargs):
# 		context = super(AlterationCreateView, self).get_context_data(**kwargs)
# 		context['title'] = "Settle Invoice"
# 		context['balance'] = self.balance
# 		return conte