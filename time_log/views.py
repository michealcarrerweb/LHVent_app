from __future__ import unicode_literals

import datetime
import time

from django.contrib import messages
from django.db import transaction
from django.http import HttpResponseRedirect, Http404, HttpResponseBadRequest
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.edit import ModelFormMixin

from source_utils.permission_mixins import SuperUserCheckMixin, ManagerCheckMixin
from .forms import StaffCreateForm, StaffLogUpdateForm, StaffAddToForm 
from .models import AvailabilityForDay, ScheduledTimeSlotEntry, LoggedDay


class DayAuthMixin(ManagerCheckMixin):
    model = LoggedDay


class TimeDayList(DayAuthMixin, ListView):
    template_name = "time_log/day_list.html"
    title = "Days/Time"

    # def get_context_data(self, **kwargs):
    #     context = super(AvailabilityForDayList, self).get_context_data(**kwargs)
    #     context['title'] = "{}'s Weekly Availability".format(self.staff)
    #     context['title_pk'] = self.staff.pk
    #     context['days_avail'] = self.days_avail
    #     return context

    # def get_queryset(self):
    #     try:
    #         self.staff = get_object_or_404(User, pk=self.kwargs['pk'])
    #         availability = AvailabilityForDay.objects.filter(
    #             staff=self.staff
    #         )
    #         self.days_avail = True
    #         ordered_schedule = []
    #         days_of_week = [
    #             'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 
    #             'Saturday', 'Sunday'
    #         ]
    #         for day in days_of_week:
    #             for obj in availability:
    #                 if day in obj.day:
    #                     new = {
    #                             'staff':obj.staff.pk, 
    #                             'day':obj.day, 
    #                             'start':obj.scheduled_start, 
    #                             'end':obj.scheduled_end, 
    #                             'pk':obj.pk
    #                           }
    #                     ordered_schedule.append(new)
    #         if len(ordered_schedule) == 7:
    #             self.days_avail = False
    #         return ordered_schedule
    #     except AvailabilityForDay.DoesNotExist:
    #         return redirect(reverse("/"))

        
class AvailAuthMixin(ManagerCheckMixin):
    model = AvailabilityForDay


class AvailabilityForDayList(AvailAuthMixin, ListView):
    template_name = "time_log/staff_avail_list.html"
    # title = "Staff Availability"

    def get_context_data(self, **kwargs):
        context = super(AvailabilityForDayList, self).get_context_data(**kwargs)
        context['title'] = "{}'s Weekly Availability".format(self.staff)
        context['title_pk'] = self.staff.pk
        context['days_avail'] = self.days_avail
        return context

    def get_queryset(self):
        try:
            self.staff = get_object_or_404(User, pk=self.kwargs['pk'])
            availability = AvailabilityForDay.objects.filter(
                staff=self.staff
            )
            self.days_avail = True
            ordered_schedule = []
            days_of_week = [
                'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 
                'Saturday', 'Sunday'
            ]
            for day in days_of_week:
                for obj in availability:
                    if day in obj.day:
                        new = {
                                'staff':obj.staff.pk, 
                                'day':obj.day, 
                                'start':obj.scheduled_start, 
                                'end':obj.scheduled_end, 
                                'pk':obj.pk
                              }
                        ordered_schedule.append(new)
            if len(ordered_schedule) == 7:
                self.days_avail = False
            return ordered_schedule
        except AvailabilityForDay.DoesNotExist:
            return redirect(reverse("/"))


class BaseMessageMixin(AvailAuthMixin, SuccessMessageMixin):
    success_message = "Schedule for day was successfully created"
    template_name = "form.html"

    def get_success_url(self):
        return reverse_lazy('time_log:staff_avail_list', 
            args = (self.object.staff.pk,)
        )


class AvailabilityStaffCreate(BaseMessageMixin, CreateView):
    title = "Availability For This Staff Has Not Been Created Yet"
    form_class = StaffCreateForm


class AvailabilityForDayCreate(BaseMessageMixin, CreateView):
    form_class = StaffAddToForm

    def get_context_data(self, **kwargs):
        context = super(AvailabilityForDayCreate, self).get_context_data(**kwargs)
        context['title'] = "Add to {}'s Weekly Availability".format(self.staff)
        return context

    def get_initial(self):
        initial = super(AvailabilityForDayCreate, self).get_initial()
        self.staff = get_object_or_404(User, pk=self.kwargs['pk'])
        initial["staff"] = self.staff
        return initial

    def get_form_kwargs(self):
        kwargs = super(AvailabilityForDayCreate, self).get_form_kwargs()
        DAY_OPTIONS = [
            ('Monday', 'Monday'),
            ('Tuesday', 'Tuesday'),
            ('Wednesday', 'Wednesday'),
            ('Thursday', 'Thursday'),
            ('Friday', 'Friday'),
            ('Saturday', 'Saturday'),
            ('Sunday', 'Sunday'),
        ]
        self.staff = get_object_or_404(User, pk=self.kwargs['pk'])
        if self.staff:
            days_schedule = AvailabilityForDay.objects.filter(staff=self.staff)
            for obj in days_schedule:
                DAY_OPTIONS.remove((obj.day,obj.day))
        kwargs['days_of_week'] = DAY_OPTIONS
        return kwargs


class AvailabilityForDayUpdate(BaseMessageMixin, UpdateView):
    success_message = "%(name)s schedule for %(day)s was successfully updated"
    title = "Service Category Update"
    form_class = StaffLogUpdateForm

    def get_context_data(self, **kwargs):
        context = super(AvailabilityForDayUpdate, self).get_context_data(**kwargs)
        context['title'] = "{}'s {} Availability".format(
            self.object.staff,
            self.object.day,
        )
        return context

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            name=self.object.staff,
            day=self.object.day,
        )


class AvailabilityForDayDelete(SuperUserCheckMixin, DeleteView):
    model = AvailabilityForDay
    template_name = "delete.html"
    success_message = "Schedule for day was successfully deleted"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(AvailabilityForDayDelete, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('time_log:staff_avail_list', 
            args = (self.object.staff.pk,)
        )


##############################################################
class TimeSlotAuthMixin(ManagerCheckMixin):
    model = ScheduledTimeSlotEntry


class TimeSlotMessageMixin(TimeSlotAuthMixin, SuccessMessageMixin):
    success_message = "Time Slot for day was successfully created"
    template_name = "form.html"

    # def get_success_url(self):
    #     return reverse_lazy('time_log:staff_avail_list', 
    #         args = (self.object.staff.pk,)
    #     )


class TimeSlotForActivityCreate(TimeSlotMessageMixin, CreateView):
    # form_class = StaffAddToForm

    def get_context_data(self, **kwargs):
        context = super(TimeSlotForActivityCreate, self).get_context_data(**kwargs)
        context['title'] = "Add to {} to {}".format(self.staff, self.work_order)
        return context

    def get_initial(self):
        initial = super(TimeSlotForActivityCreate, self).get_initial()
        # self.staff = get_object_or_404(User, pk=self.kwargs['pk'])
        # initial["staff"] = self.staff
        return initial

    # def get_form_kwargs(self):
    #     kwargs = super(AvailabilityForDayCreate, self).get_form_kwargs()
    #     DAY_OPTIONS = [
    #         ('Monday', 'Monday'),
    #         ('Tuesday', 'Tuesday'),
    #         ('Wednesday', 'Wednesday'),
    #         ('Thursday', 'Thursday'),
    #         ('Friday', 'Friday'),
    #         ('Saturday', 'Saturday'),
    #         ('Sunday', 'Sunday'),
    #     ]
    #     self.staff = get_object_or_404(User, pk=self.kwargs['pk'])
    #     if self.staff:
    #         days_schedule = AvailabilityForDay.objects.filter(staff=self.staff)
    #         for obj in days_schedule:
    #             DAY_OPTIONS.remove((obj.day,obj.day))
    #     kwargs['days_of_week'] = DAY_OPTIONS
    #     return kwargs


class TimeSlotsForDayList(TimeSlotAuthMixin, ListView):
    pass
    # template_name = "time_log/staff_avail_list.html"
    # title = "Staff Availabilityn"

    # def get_context_data(self, **kwargs):
    #     context = super(AvailabilityForDayList, self).get_context_data(**kwargs)
    #     context['title'] = "{}'s Weekly Availability".format(self.staff)
    #     context['title_pk'] = self.staff.pk
    #     context['days_avail'] = self.days_avail
    #     return context

    # def get_queryset(self):
    #     try:
    #         self.staff = get_object_or_404(User, pk=self.kwargs['pk'])
    #         availability = AvailabilityForDay.objects.filter(
    #             staff=self.staff
    #         )
    #         self.days_avail = True
    #         ordered_schedule = []
    #         days_of_week = [
    #             'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 
    #             'Saturday', 'Sunday'
    #         ]
    #         for day in days_of_week:
    #             for obj in availability:
    #                 if day in obj.day:
    #                     new = {
    #                             'staff':obj.staff.pk, 
    #                             'day':obj.day, 
    #                             'start':obj.scheduled_start, 
    #                             'end':obj.scheduled_end, 
    #                             'pk':obj.pk
    #                           }
    #                     ordered_schedule.append(new)
    #         if len(ordered_schedule) == 7:
    #             self.days_avail = False
    #         return ordered_schedule
    #     except AvailabilityForDay.DoesNotExist:
    #         return redirect(reverse("/"))

# class StaffLogDetail(ManagerCheckMixin, DetailView):
#     model = StaffLog
#     template_name = "time_log/staff_log_detail.html"


# # class StaffLogMessageMixin(StaffLogAuthMixin, SuccessMessageMixin):
# #     template_name = "form.html"
# #     form_class = StaffLogCreateForm

# #     def get_success_url(self):
# #         return reverse_lazy('time_log:staff_log_list', 
# #             args = (self.object.staff.pk,)
# #         )

# # class TagListView(ListView):

# #     template_name = "tag_post_list.html"

# #     def get_queryset(self):
# #         slug = self.kwargs['slug']
# #         try:
# #             tag = Tag.objects.get(slug=slug)
# #             return tag.post_set.all()
# #         except Tag.DoesNotExist:
# #             return Post.objects.none()

# class StaffLogList(ManagerCheckMixin, ListView):
#     model = StaffLog
#     template_name = "time_log/staff_log_list.html"

#     def get_queryset(self):
#         self.staff = get_object_or_404(User, pk=self.args[0])
#         try:
#             return StaffLog.objects.filter(staff=self.staff)
#         except StaffLog.DoesNotExist:
#             return redirect(reverse("time_log:staff_log_create"), self.get_success_message())

#     def get_context_data(self, **kwargs):
#         context = super(StaffLogList, self).get_context_data(**kwargs)
#         context['title'] = "{}'s Work Week Schedule".format(self.staff.username)
#         return context
    


# class StaffLogCreate(ManagerCheckMixin, SuccessMessageMixin, CreateView):
#     model = StaffLog
#     success_message = "%(base)s's schedule for %(day)ss was successfully created"
#     form_class = StaffLogCreateForm
#     template_name = "form.html"

#     def get_context_data(self, **kwargs):
#         context = super(StaffLogCreate, self).get_context_data(**kwargs)
#         user = User.objects.get(id=self.id)
#         self.username = user.username
#         context['title'] = "{} Log Create".format(user.username)
#         return context

#     def get_success_message(self, cleaned_data):
#         return self.success_message % dict(
#             cleaned_data,
#             base=self.object.staff.username,
#             day=self.object.day,
#         )

#     # def get_initial(self):
#     #     initial = super(StaffLogCreate, self).get_initial()
#     #     user = User.get(id=self.id)
#     #     initial["staff"] = user.username
#     #     return initial

#     def get_initial(self):
#         staff = get_object_or_404(User, id=self.kwargs.get('id')) #slug=self.kwargs.get('slug'))
#         return {
#             'staff':staff,
#         }

#     def get_success_url(self):
#         return reverse_lazy('time_log:staff_log_list', 
#             args = (self.object.staff.pk,)
#         )


# # class StaffAndTimeCreate(StaffLogMessageMixin, CreateView):
# #     template_name = "time_log/staff_time_form.html"
# #     form_class = StaffCreateForm 
# #     success_url = reverse_lazy('time_log:staff_list')
# #     success_message = "%(log)s was successfully created"

# #     def get_context_data(self, **kwargs):
# #         data = super(StaffAndTimeCreate, self).get_context_data(**kwargs)
# #         data['title'] = "Create Staff Log"
# #         if self.request.POST:
# #             data['partmembers'] = StaffAndTimeFormSet(self.request.POST)
# #         else:
# #             data['partmembers'] = StaffAndTimeFormSet()
# #         return data

# #     def form_valid(self, form):
# #         context = self.get_context_data()
# #         partmembers = context['partmembers']
# #         with transaction.atomic():
# #             self.object = form.save()

# #             if partmembers.is_valid():
# #                 partmembers.instance = self.object
# #                 partmembers.save()
# #         return super(StaffAndTimeCreate, self).form_valid(form)

#     # def get_success_message(self, cleaned_data):
#     #     return self.success_message % dict(
#     #         cleaned_data,
#     #         log=self.object.staff,
#     #     )


# # class StaffLogUpdate(StaffLogMessageMixin, UpdateView):
# #     success_message = "%(base)s was successfully updated"
# #     title = "Staff Log Update"

#     # def get_success_message(self, cleaned_data):
#     #     return self.success_message % dict(
#     #         cleaned_data,
#     #         base=self.object.staff,
#     #     )


# class StaffLogDelete(SuperUserCheckMixin, DeleteView):
#     model = StaffLog
#     template_name = "delete.html"
#     success_url = reverse_lazy('time_log:staff_log_list')
#     success_message = "Log was successfully deleted"

#     def delete(self, request, *args, **kwargs):
#         messages.success(self.request, self.success_message)
#         return super(StaffLogDelete, self).delete(request, *args, **kwargs)

