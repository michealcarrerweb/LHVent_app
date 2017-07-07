from __future__ import unicode_literals

import datetime
import time

from django.contrib import messages
from django.db import transaction
from django.http import HttpResponseRedirect, Http404, HttpResponseBadRequest
# from employee.models import Employee
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.edit import ModelFormMixin

from source_utils.permission_mixins import SuperUserCheckMixin, ManagerCheckMixin
from .forms import StaffCreateForm, StaffLogCreateForm, StaffAndTimeFormSet
from .models import StaffLog


class StaffLogAuthMixin(ManagerCheckMixin):
    model = StaffLog
    title = ""

    def get_context_data(self, **kwargs):
        context = super(StaffLogAuthMixin, self).get_context_data(**kwargs)
        context['title'] = self.title
        return context


class StaffLogDetail(StaffLogAuthMixin, DetailView):
    template_name = "time_log/staff_log_detail.html"


class StaffList(StaffLogAuthMixin, ListView):
    # template_name = "time_log/staff_list.html"
    # context_object_name = 'staff_list'
    # queryset = User.objects.filter(is_staff=True).exclude(pk=1)
    # title = "Staff"
    pass


class ClientList(StaffLogAuthMixin, ListView):
    # template_name = "time_log/client_list.html"
    # context_object_name = 'client_list'
    # queryset = User.objects.filter(is_client=True)
    # title = "Clients"
    pass


class StaffLogMessageMixin(StaffLogAuthMixin, SuccessMessageMixin):
    template_name = "form.html"
    form_class = StaffLogCreateForm

    # def get_success_url(self):
    #     return reverse_lazy('time_log:staff_log_list', 
    #         args = (self.object.staff.pk,)
    #     )

# class TagListView(ListView):

#     template_name = "tag_post_list.html"

#     def get_queryset(self):
#         slug = self.kwargs['slug']
#         try:
#             tag = Tag.objects.get(slug=slug)
#             return tag.post_set.all()
#         except Tag.DoesNotExist:
#             return Post.objects.none()

class StaffLogList(StaffLogAuthMixin, ListView):
    template_name = "time_log/staff_log_list.html"

    # def get_queryset(self):
    #     self.staff = get_object_or_404(User, pk=self.args[0])
    #     try:
    #         return StaffLog.objects.filter(staff=self.staff)
    #     except StaffLog.DoesNotExist:
    #         return redirect(reverse("time_log:staff_log_create"), self.get_success_message())

    # def get_context_data(self, **kwargs):
    #     context = super(StaffLogList, self).get_context_data(**kwargs)
    #     context['title'] = "{}'s Week Work Schedule".format(self.staff)
    #     return context
    pass


class StaffLogCreate(StaffLogMessageMixin, CreateView):
    success_message = "%(base)s was successfully created"
    title = "Staff Log Create"

    # def get_success_message(self, cleaned_data):
    #     return self.success_message % dict(
    #         cleaned_data,
    #         base=self.object.staff,
    #     )


class StaffAndTimeCreate(StaffLogMessageMixin, CreateView):
    template_name = "time_log/staff_time_form.html"
    form_class = StaffCreateForm 
    success_url = reverse_lazy('time_log:staff_list')
    success_message = "%(log)s was successfully created"

    def get_context_data(self, **kwargs):
        data = super(StaffAndTimeCreate, self).get_context_data(**kwargs)
        data['title'] = "Create Staff Log"
        if self.request.POST:
            data['partmembers'] = StaffAndTimeFormSet(self.request.POST)
        else:
            data['partmembers'] = StaffAndTimeFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        partmembers = context['partmembers']
        with transaction.atomic():
            self.object = form.save()

            if partmembers.is_valid():
                partmembers.instance = self.object
                partmembers.save()
        return super(StaffAndTimeCreate, self).form_valid(form)

    # def get_success_message(self, cleaned_data):
    #     return self.success_message % dict(
    #         cleaned_data,
    #         log=self.object.staff,
    #     )


class StaffLogUpdate(StaffLogMessageMixin, UpdateView):
    success_message = "%(base)s was successfully updated"
    title = "Staff Log Update"

    # def get_success_message(self, cleaned_data):
    #     return self.success_message % dict(
    #         cleaned_data,
    #         base=self.object.staff,
    #     )


class StaffLogDelete(SuperUserCheckMixin, DeleteView):
    model = StaffLog
    template_name = "delete.html"
    success_url = reverse_lazy('time_log:staff_log_list')
    success_message = "Log was successfully deleted"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(StaffLogDelete, self).delete(request, *args, **kwargs)

