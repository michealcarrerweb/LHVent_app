from __future__ import unicode_literals

from django.conf.urls import url
from django.contrib import admin

from .views import (
	OrderList, OrderCreate, OrderDetail, OrderUpdate, OrderDelete,
	OrderPulled, OrderCompleted
)


app_name = 'work_order'
urlpatterns = [
	
	url(r'^orders/$', OrderList.as_view(), 
		name="order_list"),
	url(r'^order/add/$', OrderCreate.as_view(), 
		name="order_add"),	
	url(r'^order/(?P<slug>[-\w]+)/$', OrderDetail.as_view(), 
		name="order_detail"),
	url(r'^order/(?P<slug>[-\w]+)/update/$', OrderUpdate.as_view(), 
		name="order_update"),
	url(r'^order/(?P<slug>[-\w]+)/delete/$', OrderDelete.as_view(), 
		name="order_delete"),

	url(r'^order/(?P<slug>[-\w]+)/pulled/$', OrderPulled.as_view(), 
		name="order_pulled"),
	url(r'^order/(?P<slug>[-\w]+)/work_completed/$', OrderCompleted.as_view(), 
		name="work_completed"),
]

	# scheduled = models.BooleanField(
#         default=False
#     )
#     completed = models.BooleanField(
#         default=False
#     )
#     sent_to_finance = models.BooleanField(
#         default=False
#     )
#     postponed = models.BooleanField(
#         verbose_name="Order postponed", 
#         default=False
#     )
#     pulled = models.DateTimeField(
#         "Product pulled", 
#         blank=True, 
#         null=True
#     )
#     work_initiated = models.DateTimeField(
#         blank=True, 
#         null=True
#     )   
#     work_completed = models.DateTimeField(
#         blank=True, 
#         null=True
#     )
#     order_created = models.DateField(
#         auto_now_add=True
#     )      
#     closed_out