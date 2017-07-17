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
from .forms import OrderPulledForm, OrderCompletedForm
from stock.models import Product


class OrderAuthMixin(ManagerCheckMixin):
	model = Order
	title = ""

	def get_context_data(self, **kwargs):
		context = super(OrderAuthMixin, self).get_context_data(**kwargs)
		context['title'] = self.title
		return context


class OrderList(OrderAuthMixin, ListView):
	template_name = "work_order/order_list.html"
	title = "Order List"


class OrderDetail(OrderAuthMixin, DetailView):
	template_name = "work_order/order_detail.html"

	def get_context_data(self, **kwargs):
		context = super(OrderDetail, self).get_context_data(**kwargs)
		all_time, all_cost, parts_list = self.object.get_services_parts_time_cost_list()
		context['all_time'] = all_time
		context['all_cost'] = all_cost
		context['parts_list'] = parts_list
		context['title'] = self.__str__()

		return context


class OrderMessageMixin(OrderAuthMixin, SuccessMessageMixin):
	template_name = "form.html"
	success_url = reverse_lazy('work_order:order_list')

	def get_success_message(self, cleaned_data):
		name = self.object.client.first_name
		if self.object.client.account.spouse_name:
			name += " and " + self.object.client.account.spouse_name
		identifier = "{} {} - {} ({})".format(
			name, self.object.client.last_name, self.object.description,
			str(self.object.order_created)
		)
		return self.success_message % dict(
			cleaned_data,
			order=identifier,
		)


class OrderCreate(OrderMessageMixin, CreateView):
	fields = ["client", "description", "note", "services"]
	success_message = "%(order)s was successfully created"
	title = "Create Order"


class OrderUpdate(OrderMessageMixin, UpdateView):
	fields = ["client", "description", "note", "services", "postponed"]
	success_message = "%(order)s was successfully updated"
	title = "Update Order"


class OrderPulled(OrderMessageMixin, UpdateView):
	form_class = OrderPulledForm
	success_message = "%(order)s is marked as pulled"

	def get_initial(self):
		return {
			'pulled':datetime.now()
		}


	def get_context_data(self, **kwargs):
		context = super(OrderPulled, self).get_context_data(**kwargs)
		context['title'] = "Are you sure that all the products for {} are pulled?".format(
			self.object.__str__()
		)
		return context

	def form_valid(self, form):
		if not "pulled product" in self.object.job_history:
			for service in self.object.services.all():
				for part in service.parts.all():
					items = Product.objects.filter(item=part.product)
					for item in items:
						item.quantity_called_for += part.quantity
					item.save()
			self.object.job_history += "{} pulled product - {}\n".format(
			self.request.user.username,
			str(datetime.now().strftime(
			"%Y-%m-%d %H:%M:%S"))
			)
		return super(OrderPulled, self).form_valid(form)


class OrderCompleted(OrderMessageMixin, UpdateView):
	form_class = OrderCompletedForm
	success_message = "%(order)s is marked as completed!"

	def get_initial(self):
		return {
			'work_completed':datetime.now()
		}


	def get_context_data(self, **kwargs):
		context = super(OrderCompleted, self).get_context_data(**kwargs)
		context['title'] = "Are you sure that {} is completed?".format(
			self.object.__str__()
		)
		return context

	def form_valid(self, form):
		if "Work completed" not in self.object.job_history:
			for service in self.object.services.all():
				for part in service.parts.all():
					items = Product.objects.filter(item=part.product)
					for item in items:
						item.quantity_called_for -= part.quantity
						item.quantity -= part.quantity
					item.save()
			self.object.job_history += "Work completed by {} - {}\n".format(
                self.request.user.username,
                str(datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"))
                )
		return super(OrderCompleted, self).form_valid(form)


class OrderDelete(SuperUserCheckMixin, DeleteView):
	model = Order
	template_name = "delete.html"
	success_url = reverse_lazy('work_order:order_list')
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
