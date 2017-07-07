from __future__ import unicode_literals

from django.conf.urls import url
from django.contrib import admin

from .views import (
	StaffLogDetail, StaffLogList, StaffLogCreate, StaffLogUpdate, 
	StaffLogDelete, StaffAndTimeCreate, StaffList, ClientList
)


app_name = 'time_log'
urlpatterns = [

	url(r'^staff/$', StaffList.as_view(), 
					name="staff_list"),
	url(r'^clients/$', ClientList.as_view(), 
					name="client_list"),

	url(r'^staff_log/(\d+)/$', StaffLogList.as_view(), 
					name="staff_log_list"),	
	url(r'^staff_log/create/$', StaffLogCreate.as_view(), 
					name="staff_log_create"),	
	url(r'^staff_log/(?P<slug>[-\w]+)/$', StaffLogDetail.as_view(), 
					name="staff_log_detail"),
	url(r'^staff_log/(?P<slug>[-\w]+)/update/$', StaffLogUpdate.as_view(), 
					name="staff_log_update"),
	url(r'^staff_log/(?P<slug>[-\w]+)/delete/$', StaffLogDelete.as_view(), 
					name="staff_log_delete"),

]