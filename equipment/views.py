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
	title = ""

	def get_context_data(self, **kwargs):
		context = super(BaseMixin, self).get_context_data(**kwargs)
		context['title'] = self.title
		return context


class BaseTypeDetail(BaseMixin, DetailView):
	template_name = "equipment/base_detail.html"


class BaseTypeList(BaseMixin, ListView):
	template_name = "equipment/base_list.html"
	title = "Tool Categories"


class BaseSuccessMixin(BaseMixin, SuccessMessageMixin):
	template_name = "form.html"
	form_class = BaseForm
	success_url = reverse_lazy('equipment:base_list')


class BaseTypeCreate(BaseSuccessMixin, CreateView):
	success_message = "%(base)s was successfully created"
	title = "Tool Category Create"

	def get_success_message(self, cleaned_data):
		return self.success_message % dict(
			cleaned_data,
			base=self.object.category,
		)


class BaseTypeUpdate(BaseSuccessMixin, UpdateView):
	success_message = "%(base)s was successfully updated"
	title = "Tool Category Update"

	def dispatch(self, request, *args, **kwargs):
		if "personal-tools" in request.path:
			return redirect(self.user_check_failure_path)
		return super(BaseTypeUpdate, self).dispatch(request, *args, **kwargs)

	def get_success_message(self, cleaned_data):
		return self.success_message % dict(
			cleaned_data,
			base=self.object.category,
		)


class BaseTypeDelete(SuperUserCheckMixin, DeleteView):
	model = Base
	template_name = "delete.html"
	success_url = reverse_lazy('equipment:base_list')
	success_message = "Category was successfully deleted"

	def dispatch(self, request, *args, **kwargs):
		if "personal-tools" in request.path:
			return redirect(self.user_check_failure_path)
		return super(BaseTypeDelete, self).dispatch(request, *args, **kwargs)

	def delete(self, request, *args, **kwargs):
		messages.success(self.request, self.success_message)
		return super(BaseTypeDelete, self).delete(request, *args, **kwargs)


class JobToolMixin(MaintenanceAndManagerCheckMixin):
	model = JobTool


class JobToolDetail(JobToolMixin, DetailView):
	template_name = "equipment/job_tool_detail.html"


class JobToolCategoryList(MaintenanceAndManagerCheckMixin, ListView):
	template_name = "equipment/job_tool_to_category_list.html"

	def get_queryset(self):
		self.category = get_object_or_404(Base, slug=self.args[0])
		return JobTool.objects.filter(base=self.category)

	def get_context_data(self, **kwargs):
		context = super(JobToolCategoryList, self).get_context_data(**kwargs)
		context['title'] = self.category
		return context


class BasicToolList(JobToolMixin, ListView):
	template_name = "equipment/basic_tool_list.html"
	title = "All basic tools"

	def get_queryset(self):
		return JobTool.objects.filter(tool_type="personal")


class JobToolSuccessMixin(JobToolMixin, SuccessMessageMixin):
	template_name = "form.html"
	form_class = JobToolForm
	success_url = reverse_lazy('equipment:base_list')


class JobToolCreate(JobToolSuccessMixin, CreateView):
	success_message = "%(tool)s was successfully created"
	title = "Add job tool"

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
	title = "Update tool"

	def get_success_message(self, cleaned_data):
		return self.success_message % dict(
			cleaned_data,
			tool=self.object.tool,
		)


class JobToolDelete(DeleteViewMixin, DeleteView):
	model = JobTool
	success_url = reverse_lazy('equipment:base_list')

