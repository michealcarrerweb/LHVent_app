from __future__ import unicode_literals

from decimal import Decimal
from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .forms import GiveQuoteForm, ResolutionForm, SettleForm, CloseOutForm
from .models import Invoice, InvoiceAlteration, CustomerConflict
from source_utils.permission_mixins import FinanceCheckMixin, SuperUserCheckMixin
from source_utils.view_mixins import DeleteViewMixin
from source_utils.starters import Conflict


from reportlab.pdfgen import canvas
from django.http import HttpResponse

from .printing import MyPrint
from io import BytesIO


def print_users(request, slug):
    invoice = get_object_or_404(Invoice, slug=slug)
    if invoice.work_order.work_completed and not invoice.due_by:
        invoice.due_by = datetime.now()+timedelta(days=35)
        invoice.save()

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


class InvoicesOptionsListView(InvoiceMixin, ListView):
    success_url = reverse_lazy('customer_finance:invoice_lists')
    template_name = "customer_finance/optional_lists.html"
    paginate_by = 4

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


class InvoiceDetailView(InvoiceMixin, DetailView):
    template_name = "customer_finance/invoice_detail.html"
    url_insert = "customer_finance:invoice_delete"

    def get_context_data(self, **kwargs):
        context = super(InvoiceDetailView, self).get_context_data(**kwargs)
        context['total_after_tax'] = self.object.invoice_quote.total_price_quoted
        context['total_tax'] = self.object.invoice_quote.tax_on_quote
        context['before_tax'] = self.object.invoice_quote.total_price_quoted - self.object.invoice_quote.tax_on_quote
        context['balance_due'] = self.object.get_balance_due()
        context['payment_schedule'] = self.object.get_payment_schedule()

        return context


class InvoiceEditMixin(InvoiceMixin, SuccessMessageMixin):
    template_name = 'form.html'

    def get_success_message(self, cleaned_data):
    	project_name = "{} - {}".format(
    		self.object.work_order.client.full_family_name(), 
    		self.object.work_order.description)
    	return self.success_message % dict(
    		cleaned_data,
    		item=project_name
    	)


class InvoiceCreateView(InvoiceEditMixin, CreateView):
    success_message = "%(item)s was successfully created"
    title = "New Invoice"
    fields = ["work_order", "pricing", "tax", "note"]


class InvoiceUpdateView(InvoiceCreateView):
    success_message = "%(item)s was successfully updated"
    title = "Update Invoice"
    fields = ["pricing", "tax", "note"]


class InvoiceGiveQuoteView(InvoiceEditMixin, UpdateView):
    success_message = "%(item)s was successfully quoted"
    title = "Quote Invoice"
    form_class = GiveQuoteForm

    def form_valid(self, form):
        self.object.give_price_quote = True
        self.object = form.save()
        return super(InvoiceGiveQuoteView, self).form_valid(form)


class InvoiceCloseOutView(InvoiceEditMixin, UpdateView):
    success_message = "%(item)s was successfully closed out"
    form_class = CloseOutForm

    def get_initial(self):
        # self.get_the_data()
        initial = super(InvoiceCloseOutView, self).get_initial()
        initial['closed_out'] = True

        return initial

    def get_context_data(self, **kwargs):
        context = super(InvoiceCloseOutView, self).get_context_data(**kwargs)
        context['title'] = "Close Out \"{}\"".format(self.object)
        return context

    def form_valid(self, form):
        self.object.log += "Invoice closed out on {} by {}\n".format(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            self.request.user,
            )
        self.object = form.save()
        return super(InvoiceCloseOutView, self).form_valid(form)


class InvoiceDeleteView(DeleteViewMixin):
    model = Invoice
    success_url = reverse_lazy('customer_finance:invoice_lists', args=['active'])


# class InvoiceDeleteView(DeleteViewMixin):
#     model = Invoice
#     template_name = "delete.html"
#     success_url = reverse_lazy('customer_finance:invoice_lists', args=['active'])
#     success_message = "Order was successfully deleted"

#     def delete(self, request, *args, **kwargs):
#         obj = self.get_object()
#         obj.work_order.sent_to_finance = False
#         obj.work_order.save()
#         messages.success(self.request, self.success_message)
#         return super(InvoiceDeleteView, self).delete(request, *args, **kwargs)


class AlterationMixin(FinanceCheckMixin):
    model = InvoiceAlteration


class AlterationDetailView(AlterationMixin, DetailView):
    template_name = "customer_finance/alteration_detail.html"


class AlterationByInvoiceListView(AlterationMixin, ListView):
    template_name = "customer_finance/alteration_list.html"

    def get_queryset(self):
        self.this_invoice = get_object_or_404(Invoice, slug=self.args[0])
        return InvoiceAlteration.objects.filter(invoice=self.this_invoice)

    def get_context_data(self, **kwargs):
        context = super(
            AlterationByInvoiceListView, self).get_context_data(**kwargs
        )
        context['title'] = "Alteration for {}".format(self.this_invoice)
        return context


class AlterationCreateView(AlterationMixin, SuccessMessageMixin, CreateView):
    template_name = 'form.html'
    form_class = SettleForm
    success_message = "$%(item)s was successfully %(action)s to %(location)s"

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

    def get_success_message(self, cleaned_data):
        project_name = "{} - {}".format(
            self.object.invoice.work_order.client.full_family_name(), 
            self.object.invoice.work_order.description)
        return self.success_message % dict(
            cleaned_data,
            item=self.object.transaction_amount,
            action=self.object.transaction_update,
            location=project_name
        )


class ConflictMixin(FinanceCheckMixin):
    model = CustomerConflict


class CustomerConflictMixin(ConflictMixin, SuccessMessageMixin):
    success_message = "Conflict was successfully %(action)s invoice %(location)s"
    template_name = 'form.html'
    action = "added to"

    def get_success_url(self):
        return reverse('customer_finance:invoice_lists', args=["conflicted"])

    def get_success_message(self, cleaned_data):
        project_name = "{} - {}".format(
            self.object.invoice.work_order.client.full_family_name(), 
            self.object.invoice.work_order.description)
        return self.success_message % dict(
            cleaned_data,
            action=self.action,
            location=project_name
        )


class CustomerConflictCreateView(CustomerConflictMixin, CreateView):
    fields = ["invoice", "conflict_description"]

    def get_initial(self):
        self.invoice = get_object_or_404(Invoice, slug=self.kwargs.get('slug'))
        return {
            'invoice':self.invoice,
        }

    def get_context_data(self, **kwargs):
        context = super(CustomerConflictCreateView, self).get_context_data(**kwargs)
        context['title'] = "New Conflict for {}".format(self.invoice)
        return context


class CustomerConflictUpdateView(CustomerConflictMixin, UpdateView):
    fields = ["conflict_description"]

    def get_context_data(self, **kwargs):
        context = super(CustomerConflictUpdateView, self).get_context_data(**kwargs)
        context['title'] = "Update Conflict for {}".format(self.object.invoice)
        return context


class CustomerConflictResolveView(CustomerConflictMixin, UpdateView):
    form_class = ResolutionForm
    action = "resolved for"

    def get_context_data(self, **kwargs):
        context = super(CustomerConflictResolveView, self).get_context_data(**kwargs)
        context['title'] = "Resolve Conflict for {}".format(self.object.invoice)
        return context
