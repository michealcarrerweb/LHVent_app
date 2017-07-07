from __future__ import unicode_literals

from django.conf.urls import url
from django.contrib import admin

from .views import (
    BaseTypeList, BaseTypeCreate, BaseTypeDetail, BaseTypeUpdate, 
    BaseTypeDelete, ServiceList, ServiceAndPartsCreate, ServiceDetail, 
    ServiceAndPartsUpdate, ServiceDelete, ServiceAndBaseList, 
)


app_name = 'service'
urlpatterns = [
    url(r'^base/$', BaseTypeList.as_view(),
    	name="base_service_list"),	
    url(r'^base/create/$', BaseTypeCreate.as_view(), 
    	name="base_service_create"),	
    url(r'^base/(?P<slug>[-\w]+)/$', BaseTypeDetail.as_view(), 
    	name="base_service_detail"),
    url(r'^base/(?P<slug>[-\w]+)/update/$', BaseTypeUpdate.as_view(), 
    	name="base_service_update"),
    url(r'^base/(?P<slug>[-\w]+)/delete/$', BaseTypeDelete.as_view(), 
    	name="base_service_delete"),

    url(r'^service/$', ServiceList.as_view(), 
    	name="service_list"),	
    url(r'^service/create/(?P<slug>[-\w]+)/$', ServiceAndPartsCreate.as_view(), 
    	name="service_create"),	
    url(r'^service/(?P<slug>[-\w]+)/$', ServiceDetail.as_view(), 
    	name="service_detail"),
    url(r'^service/(?P<slug>[-\w]+)/update/$', ServiceAndPartsUpdate.as_view(), 
    	name="service_update"),
    url(r'^service/(?P<slug>[-\w]+)/delete/$', ServiceDelete.as_view(), 
    	name="service_delete"),

    url(r'^service_base/([\w-]+)/$', ServiceAndBaseList.as_view(), 
    	name="service_for_base_list"),
]
