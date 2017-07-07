from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import (
	CreateView, 
	UpdateView, 
	DeleteView, 
	FormView
)
from .forms import (
	CompanyCreateForm, 
	CompanyUpdateForm
)
from .models import Company
from source_utils.permission_mixins import (
	SuperUserCheckMixin, 
	ManagerCheckMixin,
	WarehouseAndManagerCheckMixin
)


class CompanyAuthMixin(ManagerCheckMixin):
	model = Company
	title = ""

	def get_context_data(self, **kwargs):
		context = super(CompanyAuthMixin, self).get_context_data(**kwargs)
		context['title'] = self.title
		return context


class CompanyDetail(CompanyAuthMixin, DetailView):
	template_name = "product/company_detail.html"


class CompanyList(CompanyAuthMixin, ListView):
	template_name = "product/company_list.html"
	title = "Suppliers"


class CompanyMessageMixin(CompanyAuthMixin, SuccessMessageMixin):
	template_name = "form.html"
	success_url = reverse_lazy('product:company_list')


class CompanyCreate(CompanyMessageMixin, CreateView):
	success_message = "%(company)s was successfully created"
	form_class = CompanyCreateForm
	title = "Supplier Create"

	def get_success_message(self, cleaned_data):
		return self.success_message % dict(
			cleaned_data,
			company=self.object.company,
		)


class CompanyUpdate(CompanyMessageMixin, UpdateView):
	success_message = "%(company)s was successfully updated"
	form_class = CompanyUpdateForm
	title = "Supplier Update"
	user_check_failure_path = '403'

	def get_success_message(self, cleaned_data):
		return self.success_message % dict(
			cleaned_data,
			company=self.object.company,
		)

	def dispatch(self, request, *args, **kwargs):
		if "any-store" in request.path:
			return redirect(self.user_check_failure_path)
		return super(CompanyUpdate, self).dispatch(request, *args, **kwargs)


class CompanyDelete(SuperUserCheckMixin, DeleteView):
	model = Company
	template_name = "delete.html"
	success_url = reverse_lazy('product:company_list')
	success_message = "Company was successfully deleted"

	def dispatch(self, request, *args, **kwargs):
		if "any-store" in request.path:
			return redirect(self.user_check_failure_path)
		return super(CompanyDelete, self).dispatch(request, *args, **kwargs)

	def delete(self, request, *args, **kwargs):
		messages.success(self.request, self.success_message)
		return super(CompanyDelete, self).delete(request, *args, **kwargs)
