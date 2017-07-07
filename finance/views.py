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
from source_utils.view_mixins import DeleteViewMixin, ContextMixin
from .forms import PricingForm, HourlyBaseForm


class PricingMixin(FinanceCheckMixin):
	model = Pricing


class PricingEditMixin(PricingMixin, ContextMixin, SuccessMessageMixin):
	template_name = 'form.html'
	form_class = PricingForm
	success_url = reverse_lazy('finance:pricing_list')

	def __init__(self, *args, **kwargs):
		super(PricingEditMixin, self).__init__(*args, **kwargs)
		self.name = "pricing"

	def get_success_message(self, cleaned_data):
		return self.success_message % dict(
			cleaned_data,
			item=self.object.pricing,
			action=self.action,
			location=self.location,
		)

class PricingListView(PricingMixin, ContextMixin, ListView):

	def __init__(self, *args, **kwargs):
		super(PricingListView, self).__init__(*args, **kwargs)
		self.name = "pricing"
		self.action = "categories"

	def get_context_data(self, **kwargs):
		context = super(PricingListView, self).get_context_data(**kwargs)
		hourly = get_object_or_404(Hourly, pk=1)
		context['hourly'] = hourly.hourly_base
		return context


class PricingDetailView(PricingMixin, DetailView):
	template_name = "finance/pricing_detail.html"


class PricingCreateView(PricingEditMixin, CreateView):

	def __init__(self, *args, **kwargs):
		super(PricingCreateView, self).__init__(*args, **kwargs)
		self.action = "add"


class PricingUpdateView(PricingEditMixin, UpdateView):

	def __init__(self, *args, **kwargs):
		super(PricingUpdateView, self).__init__(*args, **kwargs)
		self.action = "edit"


class HourlyBaseUpdateView(SuccessMessageMixin, UpdateView):
	model = Hourly
	template_name = 'form.html'
	form_class = HourlyBaseForm
	success_url = reverse_lazy('finance:pricing_list')
	success_message = "%(item)s was successfully %(action)s to %(amount)s"

	def __init__(self, *args, **kwargs):
		super(HourlyBaseUpdateView, self).__init__(*args, **kwargs)
		self.name = "hourly base"
		self.action = "changed"

	def get_context_data(self, **kwargs):
		context = super(HourlyBaseUpdateView, self).get_context_data(**kwargs)
		context['title'] = "Change Base Hourly Rate"
		return context

	def get_success_message(self, cleaned_data):
		return self.success_message % dict(
			cleaned_data,
			item="Base hourly rate",
			action=self.action,
			amount=self.object.hourly_base,
		)


class MainLedgerDetailView(FinanceCheckMixin, DetailView):
	model = Main
	template_name = "finance/master_ledger_detail.html"