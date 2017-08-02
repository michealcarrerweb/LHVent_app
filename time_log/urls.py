from __future__ import unicode_literals

from django.conf.urls import url
from django.contrib import admin

from .views import (
    AvailabilityForDayList, AvailabilityStaffCreate, AvailabilityForDayCreate, 
    AvailabilityForDayUpdate, AvailabilityForDayDelete, TimeDayList
)

# from .views import (
#     # AvailabilityForDayList, AvailabilityForDayDetail, AvailabilityForDayCreate,
#     # AvailabilityForDayUpdate, AvailabilityForDayDelete, AvailabilityStaffCreate
# )


app_name = 'time_log'
urlpatterns = [
    url(r'^day_time_availability/$', TimeDayList.as_view(), 
                    name="day_time_avail_list"),

    url(r'^staff_avail/(?P<pk>\d+)/$', AvailabilityForDayList.as_view(), 
                    name="staff_avail_list"),       
    url(r'^staff_avail/create/$', AvailabilityStaffCreate.as_view(), 
                    name="staff_initial_create"),
    url(r'^staff_avail/(?P<pk>\d+)/add/$', AvailabilityForDayCreate.as_view(), 
                    name="staff_avail_add"),
    url(r'^staff_avail/(?P<pk>\d+)/update/$', AvailabilityForDayUpdate.as_view(), 
                    name="staff_avail_update"),
    url(r'^staff_avail/(?P<pk>\d+)/delete/$', AvailabilityForDayDelete.as_view(), 
                    name="staff_avail_delete"),

    # url(r'^staff_avail/(?P<pk>\d+)/$', AvailabilityForDayList.as_view(), 
    #                 name="staff_avail_list"),       
    # url(r'^staff_avail/create/$', AvailabilityStaffCreate.as_view(), 
    #                 name="staff_initial_create"),
    # url(r'^staff_avail/(?P<pk>\d+)/add/$', AvailabilityForDayCreate.as_view(), 
    #                 name="staff_avail_add"),
    # url(r'^staff_avail/(?P<pk>\d+)/update/$', AvailabilityForDayUpdate.as_view(), 
    #                 name="staff_avail_update"),
    # url(r'^staff_avail/(?P<pk>\d+)/delete/$', AvailabilityForDayDelete.as_view(), 
    #                 name="staff_avail_delete"),
]