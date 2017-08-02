from __future__ import unicode_literals

from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.views.generic.edit import ModelFormMixin

from hourly.models import Hourly

from .models import Pricing, Main
from source_utils.permission_mixins import FinanceCheckMixin, SuperUserCheckMixin
from source_utils.view_mixins import DeleteViewMixin
from .forms import PricingForm, HourlyBaseForm


class PricingMixin(FinanceCheckMixin):
    model = Pricing


class PricingListView(PricingMixin, ListView):

    def get_context_data(self, **kwargs):
        context = super(PricingListView, self).get_context_data(**kwargs)
        hourly = get_object_or_404(Hourly, pk=1)
        context['hourly'] = hourly.hourly_base
        return context


class PricingDetailView(PricingMixin, DetailView):
    template_name = "finance/pricing_detail.html"


class PricingEditMixin(PricingMixin, SuccessMessageMixin):
    template_name = 'form.html'
    form_class = PricingForm
    success_url = reverse_lazy('finance:pricing_list')


class PricingCreateView(PricingEditMixin, CreateView):
    success_message = "Pricing was successfully created"


class PricingUpdateView(PricingEditMixin, UpdateView):
    success_message = "Pricing was successfully updated"


class HourlyBaseUpdateView(SuccessMessageMixin, UpdateView):
    model = Hourly
    template_name = 'form.html'
    form_class = HourlyBaseForm
    success_url = reverse_lazy('finance:pricing_list')
    success_message = "Base hourly rate was successfully changed to %(amount)s"

    def get_context_data(self, **kwargs):
        context = super(HourlyBaseUpdateView, self).get_context_data(**kwargs)
        context['title'] = "Change Base Hourly Rate"
        return context

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            amount=self.object.hourly_base,
        )


class MainLedgerDetailView(FinanceCheckMixin, DetailView):
    model = Main
    template_name = "finance/master_ledger_detail.html"

    def get_context_data(self, **kwargs):
        context = super(MainLedgerDetailView, self).get_context_data(**kwargs)
        (
            total, 
            taxes,
            profit, 
            customers_balances, 
            customers_count, 
            customers_conflicts, 
            customers_unresolved_conflicts,
            projected_before_tax
        ) = self.object.get_customer_balance_sheet()

        context['customers_total'] = total
        context['customers_taxes'] = taxes
        context['customers_profit'] = profit
        context['customers_balances'] = customers_balances
        context['customers_count'] = customers_count
        context['customers_conflicts'] = customers_conflicts
        context['customers_unresolved_conflicts'] = customers_unresolved_conflicts
        context['projected_before_tax'] = projected_before_tax
        (
            expenses, 
            operation_balances, 
            operation_count, 
            operation_conflicts, 
            operation_unresolved_conflicts
        ) = self.object.get_operation_balance_sheet()
        context['operation_expenses'] = expenses
        context['operation_balances'] = operation_balances
        context['operation_count'] = operation_count
        context['operation_conflicts'] = operation_conflicts
        context['operation_unresolved_conflicts'] = operation_unresolved_conflicts
        context['net_profit'] = profit - expenses        
        return context
