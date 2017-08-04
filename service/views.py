from __future__ import unicode_literals

from django.contrib import messages
from django.db import transaction
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.views.generic.edit import ModelFormMixin

from source_utils.permission_mixins import (
    SuperUserCheckMixin, ManagerCheckMixin
)
from source_utils.view_mixins import DeleteViewMixin
from .models import Base, Service, PartsForService
from .forms import (
    BaseForm, ServiceCreateForm, ServiceUpdateForm, PartsForServiceFormSet
)
from hourly.models import Hourly


class BaseAuthMixin(ManagerCheckMixin):
    model = Base


class BaseTypeList(BaseAuthMixin, ListView):
    template_name = "service/base_list.html"
    title = "Service Categories"


class BaseTypeDetail(BaseAuthMixin, DetailView):
    template_name = "service/base_detail.html"
    url_insert = "service:invoice_delete"


class BaseMessageMixin(BaseAuthMixin, SuccessMessageMixin):
    template_name = "form.html"
    form_class = BaseForm
    success_url = reverse_lazy('service:base_service_list')


class BaseTypeCreate(BaseMessageMixin, CreateView):
    success_message = "%(base)s was successfully created"
    title = "Service Category Create"

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            base=self.object.category,
        )


class BaseTypeUpdate(BaseMessageMixin, UpdateView):
    success_message = "%(base)s was successfully updated"
    title = "Service Category Update"

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            base=self.object.category,
        )


class BaseTypeDelete(DeleteViewMixin):
    model = Base
    success_url = reverse_lazy('service:base_service_list')
    success_message = "Category was successfully deleted"


class ServiceAndBaseList(ManagerCheckMixin, ListView):#
    template_name = "service/base_to_service_list.html"

    def get_queryset(self):
        self.category = get_object_or_404(Base, slug=self.args[0])
        return Service.objects.filter(base=self.category)

    def get_context_data(self, **kwargs):
        context = super(ServiceAndBaseList, self).get_context_data(**kwargs)
        context['title'] = self.category
        return context


class ServiceDetail(ManagerCheckMixin, DetailView):#
    model = Service
    template_name = "service/service_detail.html"

    def get_context_data(self, **kwargs):
        context = super(ServiceDetail, self).get_context_data(**kwargs)
        (
            context['all_time'], 
            context['all_cost'], 
            context['parts_list']
        ) = self.object.get_parts_time_cost_list()
        return context

    def get_initial(self):
        base = get_object_or_404(Base, slug=self.kwargs.get('slug'))
        return {
            'base':base,
        }


class ServiceList(ManagerCheckMixin, ListView):#
    model = Service
    template_name = "service/service_list.html"

    def get_context_data(self, **kwargs):
        context = super(ServiceList, self).get_context_data(**kwargs)
        context['title'] = "Services"
        return context


class ServiceAndPartsCreate(ManagerCheckMixin, SuccessMessageMixin, CreateView):#
    model = Service
    template_name = "service/service_parts_form.html"
    form_class = ServiceCreateForm 
    success_url = reverse_lazy('service:base_service_list')
    success_message = "%(service)s was successfully created"

    def get_initial(self):
        self.base = get_object_or_404(Base, slug=self.kwargs.get('slug'))
        return {
            'base':self.base
        }

    def get_context_data(self, **kwargs):
        data = super(ServiceAndPartsCreate, self).get_context_data(**kwargs)
        data['title'] = "Create Service for {}".format(self.base)
        data['nav_title'] = "Create Service"
        if self.request.POST:
            data['partmembers'] = PartsForServiceFormSet(self.request.POST)
        else:
            data['partmembers'] = PartsForServiceFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        partmembers = context['partmembers']
        with transaction.atomic():
            self.object = form.save()
            if partmembers.is_valid():
                partmembers.instance = self.object
                partmembers.save()
        return super(ServiceAndPartsCreate, self).form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            service=self.object.service_description,
        )


class ServiceAndPartsUpdate(ManagerCheckMixin, SuccessMessageMixin, UpdateView):#
    model = Service
    template_name = "service/service_parts_form.html"
    form_class = ServiceUpdateForm
    success_url = reverse_lazy('service:base_service_list')
    success_message = "%(service)s was successfully updated"

    def get_context_data(self, **kwargs):
        data = super(ServiceAndPartsUpdate, self).get_context_data(**kwargs)
        data['title'] = "Update Service"
        data['nav_title'] = "Update Service"
        if self.request.POST:
            data['partmembers'] = PartsForServiceFormSet(self.request.POST, instance=self.object)
        else:
            data['partmembers'] = PartsForServiceFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        partmembers = context['partmembers']
        with transaction.atomic():
            self.object = form.save()

            if partmembers.is_valid():
                partmembers.instance = self.object
                partmembers.save()
        return super(ServiceAndPartsUpdate, self).form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            service=self.object.service_description,
        )


class ServiceDelete(DeleteViewMixin):#
    model = Service
    success_url = reverse_lazy('service:service_list')
    success_message = "Service was successfully deleted"
