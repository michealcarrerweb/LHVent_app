from __future__ import unicode_literals

from decimal import Decimal

from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .forms import GiveQuoteForm, ResolutionForm, SettleForm
from .models import Invoice, InvoiceAlteration, CustomerConflict
from source_utils.permission_mixins import FinanceCheckMixin, SuperUserCheckMixin
from source_utils.view_mixins import DeleteViewMixin, ContextMixin


from reportlab.pdfgen import canvas
from django.http import HttpResponse

from .printing import MyPrint
from io import BytesIO


def print_users(request, slug):
    title = 'attachment; first_name="{}.pdf"'.format(slug)
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename={}'.format(
    	slug + "-invoice.pdf")
 
    buffer = BytesIO()
 
    report = MyPrint(buffer, 'Letter', slug)
    pdf = report.print_users()
 
    response.write(pdf)
    return response


class InvoiceMixin(FinanceCheckMixin):
    model = Invoice


class InvoiceDetailView(InvoiceMixin, DetailView):
    template_name = "customer_finance/invoice_detail.html"


class InvoiceEditMixin(InvoiceMixin, ContextMixin, SuccessMessageMixin):
    template_name = 'form.html'
    fields = ["work_order", "pricing", "tax", "note"]

    def __init__(self, *args, **kwargs):
    	super(InvoiceEditMixin, self).__init__(*args, **kwargs)
    	self.name = "invoice"

    def get_success_message(self, cleaned_data):
    	name = self.object.work_order.client.first_name
    	if self.object.work_order.client.spouse_name:
    		name += " and " + self.object.work_order.client.spouse_name
    	project_name = "{} {} - {}".format(
    		name,
    		self.object.work_order.client.last_name, 
    		self.object.work_order.description)
    	return self.success_message % dict(
    		cleaned_data,
    		item=project_name,
    		action=self.action,
    	)


class InvoicesOptionsListView(InvoiceMixin, ListView):
    success_url = reverse_lazy('customer_finance:invoice_lists')
    template_name = "customer_finance/optional_lists.html"
    # paginate_by = 10

    def get_queryset(self):
        if self.args[0] == "owed":
            return Invoice.objects.filter(paid_in_full=False)
        elif self.args[0] == "conflicted":
            self.template_name = "customer_finance/conflicts.html"
            return CustomerConflict.objects.filter(conflict_resolution=None)
        elif self.args[0] == "active":
            return Invoice.objects.filter(closed_out=False)
        else:
            return Invoice.objects.all()

    def get_context_data(self, **kwargs):
        context = super(InvoicesOptionsListView, self).get_context_data(**kwargs)
        if self.args[0] == "owed":
            context['title'] = "Customer Invoices with Balances"
        elif self.args[0] == "conflicted":
            context['title'] = "Customer Invoices with Conflicts"
        elif self.args[0] == "active":
            context['title'] = "Active Customer Invoices"
        else:
            context['title'] = "All Customer Invoices"
        return context


class InvoiceCreateView(InvoiceEditMixin, CreateView):

    def __init__(self, *args, **kwargs):
    	super(InvoiceCreateView, self).__init__(*args, **kwargs)
    	self.action = "added"


class InvoiceGiveQuoteView(ContextMixin, SuccessMessageMixin, UpdateView):
    model = Invoice
    form_class = GiveQuoteForm
    template_name = 'form.html'

    def __init__(self, *args, **kwargs):
        super(InvoiceGiveQuoteView, self).__init__(*args, **kwargs)
        self.name = "invoice"
        self.action = "quoted"

    def get_context_data(self, **kwargs):
        context = super(InvoiceGiveQuoteView, self).get_context_data(**kwargs)
        context['title'] = "Quote Customer"
        return context

    def get_success_message(self, cleaned_data):
        name = self.object.work_order.client.first_name
        if self.object.work_order.client.spouse_name:
            name += " and " + self.object.work_order.client.spouse_name
        project_name = "{} {} - {}".format(
            name,
            self.object.work_order.client.last_name, 
            self.object.work_order.description)
        return self.success_message % dict(
            cleaned_data,
            item=project_name,
            action=self.action,
        )

    def form_valid(self, form):
        self.object.give_price_quote = True
        self.object = form.save()
        return super(InvoiceGiveQuoteView, self).form_valid(form)


class InvoiceUpdateView(InvoiceEditMixin, UpdateView):
    fields = [
    	"pricing", 
    	"note", 
    	"tax"
    ]

    def __init__(self, *args, **kwargs):
    	super(InvoiceUpdateView, self).__init__(*args, **kwargs)
    	self.action = "edit"


class InvoiceDeleteView(DeleteViewMixin):
    model = Invoice
    success_url = reverse_lazy('customer_finance:invoice_list')


class AlterationMixin(FinanceCheckMixin):
    model = InvoiceAlteration


class AlterationDetailView(AlterationMixin, DetailView):
    template_name = "customer_finance/alteration_detail.html"


class AlterationEditMixin(AlterationMixin, ContextMixin, SuccessMessageMixin):
    template_name = 'form.html'
    form_class = SettleForm

    def __init__(self, *args, **kwargs):
    	super(AlterationEditMixin, self).__init__(*args, **kwargs)
    	self.name = "alteration"

    def get_success_message(self, cleaned_data):
    	name = self.object.invoice.work_order.client.first_name
    	if self.object.invoice.work_order.client.spouse_name:
    		name += " and " + \
    		self.object.invoice.work_order.client.spouse_name
    	project_name = "{} {} - {}".format(
    		name,
    		self.object.invoice.work_order.client.last_name, 
    		self.object.invoice.work_order.description)
    	return self.success_message % dict(
    		cleaned_data,
    		item="${}".format(self.object.transaction_amount),
    		action=self.action,
    		location="to {}".format(project_name),
    	)


class AlterationByInvoiceListView(AlterationMixin, ListView):
    template_name = "customer_finance/alteration_list.html"

    def get_queryset(self):
    	self.invoice_list = get_object_or_404(Invoice, slug=self.args[0])
    	return InvoiceAlteration.objects.filter(invoice=self.invoice_list)

    def get_context_data(self, **kwargs):
    	context = super(
    		AlterationByInvoiceListView, self).get_context_data(**kwargs
    	)
    	context['title'] = "Alteration by Invoice"
    	return context


class AlterationCreateView(AlterationEditMixin, CreateView):

    def __init__(self, *args, **kwargs):
    	super(AlterationCreateView, self).__init__(*args, **kwargs)
    	self.action = "added"

    def get_initial(self):
    	self.invoice = get_object_or_404(Invoice, slug=self.kwargs.get('slug'))
    	return {
    	'invoice':self.invoice,
    	}

    def get_context_data(self, **kwargs):
    	context = super(AlterationCreateView, self).get_context_data(**kwargs)
    	context['title'] = "Settle {} Invoice".format(self.invoice)
    	context['balance'] = self.invoice.get_balance_due()
    	return context

############
class CustomerConflictMixin(FinanceCheckMixin, ContextMixin, SuccessMessageMixin):

    model = CustomerConflict
    template_name = 'form.html'

    def __init__(self, *args, **kwargs):
        super(CustomerConflictMixin, self).__init__(*args, **kwargs)
        self.name = "Conflict"

    def get_success_url(self):
        return reverse('customer_finance:invoice_lists', args=["conflicted"])

    def get_success_message(self, cleaned_data):
        name = self.object.invoice.work_order.client.first_name
        if self.object.invoice.work_order.client.spouse_name:
            name += " and " + \
            self.object.invoice.work_order.client.spouse_name
        project_name = "{} {} - {}".format(
            name,
            self.object.invoice.work_order.client.last_name, 
            self.object.invoice.work_order.description)
        return self.success_message % dict(
            cleaned_data,
            item=self.name,
            action=self.action,
            location="to " + project_name,
        )


class CustomerConflictCreateView(CustomerConflictMixin, CreateView):

    fields = [
        "invoice",
        "conflict_description"
    ]

    def __init__(self, *args, **kwargs):
        super(CustomerConflictCreateView, self).__init__(*args, **kwargs)
        self.action = "added"

    def get_initial(self):
        self.invoice = get_object_or_404(Invoice, slug=self.kwargs.get('slug'))
        return {
        'invoice':self.invoice,
        }

    def get_context_data(self, **kwargs):
        context = super(CustomerConflictCreateView, self).get_context_data(**kwargs)
        context['title'] = "New Conflict - {}".format(self.invoice)
        return context


class CustomerConflictUpdateView(CustomerConflictMixin, UpdateView):

    fields = [ 
        "conflict_description"
    ]

    def __init__(self, *args, **kwargs):
        super(CustomerConflictUpdateView, self).__init__(*args, **kwargs)
        self.action = "updated"

    def get_context_data(self, **kwargs):
        context = super(CustomerConflictUpdateView, self).get_context_data(**kwargs)
        context['title'] = "Update Conflict - {}".format(self.object.invoice)
        return context


class CustomerConflictResolveView(CustomerConflictMixin, UpdateView):
    form_class = ResolutionForm

    def __init__(self, *args, **kwargs):
        super(CustomerConflictResolveView, self).__init__(*args, **kwargs)
        self.action = "resolved"

    def get_context_data(self, **kwargs):
        context = super(CustomerConflictResolveView, self).get_context_data(**kwargs)
        context['title'] = "Resolved Conflict - {}".format(self.object.invoice)
        return context