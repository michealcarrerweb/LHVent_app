from __future__ import unicode_literals

from datetime import datetime

from django.shortcuts import render
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.utils.text import slugify

from source_utils.permission_mixins import ManagerCheckMixin, SuperUserCheckMixin

from .models import Order
from .forms import DatesLoggedForm
from stock.models import Product


class OrderAuthMixin(ManagerCheckMixin):
    model = Order
    title = ""

    def get_context_data(self, **kwargs):
        context = super(OrderAuthMixin, self).get_context_data(**kwargs)
        context['title'] = self.title
        return context


class OrderLists(OrderAuthMixin, ListView):
    template_name = "work_order/order_list.html"
    title = "Order List"
    paginate_by = 4

    def get_queryset(self):
        if self.args[0] == "not_finance":
            return Order.objects.filter(sent_to_finance=False)
        elif self.args[0] == "postponed":
            return Order.objects.exclude(postponed=None)
        elif self.args[0] == "active":
            return Order.objects.filter(closed_out=None)
        else:
            return Order.objects.all()

    def get_context_data(self, **kwargs):
        context = super(OrderLists, self).get_context_data(**kwargs)
        if self.args[0] == "not_finance":
            context['title'] = "Work Orders Not Sent To Financial"
        elif self.args[0] == "postponed":
            context['title'] = "Postponed Work Orders"
        elif self.args[0] == "active":
            context['title'] = "Active Work Orders"
        else:
            context['title'] = "All Work Orders"
        return context


class OrderDetail(OrderAuthMixin, DetailView):
    template_name = "work_order/order_detail.html"

    def get_context_data(self, **kwargs):
        context = super(OrderDetail, self).get_context_data(**kwargs)
        all_time, all_cost, parts_list = self.object.get_services_parts_time_cost_list()
        context['all_time'] = all_time
        context['all_cost'] = all_cost
        context['parts_list'] = parts_list
        context['title'] = self.object.__str__()
        context['close_out'] = self.object.check_for_close_out()

        return context


class OrderMessageMixin(OrderAuthMixin, SuccessMessageMixin):
    template_name = "form.html"
    success_url = reverse_lazy('work_order:order_list', args=['active'])
    success_message = "\"%(order)s\" has been %(action)s"
    action_mesg = ""

    def get_success_message(self, cleaned_data):
        identifier = "{} - {} ({})".format(
            self.object.client.full_family_name(), self.object.description,
            str(self.object.origin.strftime("%Y-%m-%d"))
        )
        return self.success_message % dict(
            cleaned_data,
            order=identifier,
            action=self.action_mesg,
        )


class OrderCreate(OrderMessageMixin, CreateView):
    fields = ["client", "description", "note", "services"]
    action_mesg = "created"
    title = "Create Order"


class OrderUpdate(OrderMessageMixin, UpdateView):
    fields = ["client", "description", "note", "services"]
    action_mesg = "updated"
    title = "Update Order"


class OrderAction(OrderMessageMixin, UpdateView):
    form_class = DatesLoggedForm

    def get_the_data(self, **kwargs):
        form_classes = {
            "scheduled":'scheduled',
            "pulled":'pulled',
            "initiated":'work_initiated',
            "completed":'work_completed',
            "closed":'closed_out',
            "postponed":'postponed'
            }
        for action in form_classes:
            if action == self.kwargs['action']:
                self.action_mesg = action
                self.action_choice = form_classes[action]

    def get_context_data(self, **kwargs):
        context = super(OrderAction, self).get_context_data(**kwargs)
        context['title'] = "Are you sure that \"{}\" has been {}?".format(
            self.object.__str__(),
            self.action_mesg
        )
        return context

    def get_initial(self):
        self.get_the_data()
        initial = super(OrderAction, self).get_initial()
        initial[self.action_choice] = datetime.now()

        return initial

    def form_valid(self, form):
        self.object.job_history += "{} {} order at {}\n".format(
        self.request.user.username,
        self.action_mesg,
        str(datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"))
        )
        self.object.save()
        # if self.action_mesg == "completed":
            #""" set due date for  """           
        return super(OrderAction, self).form_valid(form)


class OrderDelete(SuperUserCheckMixin, DeleteView):
    model = Order
    template_name = "delete.html"
    success_url = reverse_lazy('work_order:order_list', args=['active'])
    success_message = "Order was successfully deleted"
    user_check_failure_path = '403'

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if "pulled product" in obj.job_history:
            for service in obj.services.all():
                for part in service.parts.all():
                    items = Product.objects.filter(item=part.product)
                    for item in items:
                        item.quantity_called_for -= part.quantity
                    item.save()
        if obj.work_initiated or obj.work_completed or obj.closed_out:
            return redirect(self.user_check_failure_path)
        messages.success(self.request, self.success_message)
        return super(OrderDelete, self).delete(request, *args, **kwargs)
