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
from source_utils.view_mixins import DeleteViewMixin


class CompanyAuthMixin(WarehouseAndManagerCheckMixin):
    model = Company


class CompanyDetail(CompanyAuthMixin, DetailView):
    template_name = "company/company_detail.html"
    url_insert = "company:company_delete"


class CompanyList(CompanyAuthMixin, ListView):
    template_name = "company/company_list.html"
    title = "Supplier List"


class CompanyMessageMixin(CompanyAuthMixin, SuccessMessageMixin):
    template_name = "form.html"
    success_url = reverse_lazy('company:company_list')
    user_check_failure_path = '403'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            company=self.object.company,
        )


class CompanyCreate(CompanyMessageMixin, CreateView):
    success_message = "%(company)s was successfully created"
    form_class = CompanyCreateForm
    title = "New Supplier"


class CompanyUpdate(CompanyMessageMixin, UpdateView):
    success_message = "%(company)s was successfully updated"
    form_class = CompanyUpdateForm
    title = "Update Supplier"

    def dispatch(self, request, *args, **kwargs):
        if "any-store" in request.path:
            return redirect(self.user_check_failure_path)
        return super(CompanyUpdate, self).dispatch(request, *args, **kwargs)


class CompanyDelete(DeleteViewMixin):
    model = Company
    success_url = reverse_lazy('company:company_list')
    user_check_failure_path = '403'

    def dispatch(self, request, *args, **kwargs):
        if "any-store" in request.path:
            return redirect(self.user_check_failure_path)
        return super(CompanyDelete, self).dispatch(request, *args, **kwargs)
