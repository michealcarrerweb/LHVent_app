from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from source_utils.permission_mixins import (
    SuperUserCheckMixin,  MaintenanceAndManagerCheckMixin
)
from source_utils.view_mixins import DeleteViewMixin

from .models import Base, JobTool
from .forms import BaseForm, JobToolForm


class BaseMixin(MaintenanceAndManagerCheckMixin):
    model = Base


class BaseTypeList(BaseMixin, ListView):
    template_name = "equipment/base_list.html"
    title = "Equipment Categories"


class BaseSuccessMixin(BaseMixin, SuccessMessageMixin):
    template_name = "form.html"
    form_class = BaseForm
    success_url = reverse_lazy('equipment:base_list')

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            base=self.object.category,
        )


class BaseTypeCreate(BaseSuccessMixin, CreateView):
    success_message = "%(base)s was successfully created"
    title = "New Tool Category"


class BaseTypeUpdate(BaseSuccessMixin, UpdateView):
    success_message = "%(base)s was successfully updated"
    title = "Update Tool Category"
    url_insert = "equipment:base_delete"

    def dispatch(self, request, *args, **kwargs):
        if "personal-tools" in request.path:
            return redirect(self.user_check_failure_path)
        return super(BaseTypeUpdate, self).dispatch(request, *args, **kwargs)


class BaseTypeDelete(DeleteViewMixin):
    model = Base
    success_url = reverse_lazy('equipment:base_list')

    def dispatch(self, request, *args, **kwargs):
        if "personal-tools" in request.path:
            return redirect(self.user_check_failure_path)
        return super(BaseTypeDelete, self).dispatch(request, *args, **kwargs)


class JobToolMixin(BaseMixin):
    model = JobTool


class JobToolDetail(JobToolMixin, DetailView):
    template_name = "equipment/job_tool_detail.html"
    url_insert = "equipment:job_tool_delete"


class JobToolCategoryList(JobToolMixin, ListView):
    template_name = "equipment/job_tool_to_category_list.html"

    def get_queryset(self):
        self.category = get_object_or_404(Base, slug=self.args[0])
        return JobTool.objects.filter(base=self.category)

    def get_context_data(self, **kwargs):
        context = super(JobToolCategoryList, self).get_context_data(**kwargs)
        context['title'] = self.category
        return context


class JobToolSuccessMixin(JobToolMixin, SuccessMessageMixin):
    template_name = "form.html"
    form_class = JobToolForm
    success_url = reverse_lazy('equipment:base_list')


class JobToolCreate(JobToolSuccessMixin, CreateView):
    success_message = "%(tool)s was successfully created"
    title = "New Tool"

    def get_initial(self):
        base = get_object_or_404(Base, slug=self.kwargs.get('slug'))
        return {
            'base':base
        }

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            tool=self.object.tool,
        )


class JobToolUpdate(JobToolSuccessMixin, UpdateView):
    success_message = "%(tool)s was successfully updated"
    title = "Update Tool"

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            tool=self.object.tool,
        )


class JobToolDelete(DeleteViewMixin):
    model = JobTool
    success_url = reverse_lazy('equipment:base_list')
