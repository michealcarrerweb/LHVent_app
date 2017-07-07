from __future__ import unicode_literals

from django.conf.urls import url
from django.contrib import admin

from .views import (
    CompanyDetail, CompanyList, CompanyCreate, CompanyUpdate, 
    CompanyDelete
)


app_name = 'company'
urlpatterns = [
    url(r'^company/$', CompanyList.as_view(), 
    	name="company_list"),	
    url(r'^company/create/$', CompanyCreate.as_view(),
    	name="company_create"),	
    url(r'^company/(?P<slug>[-\w]+)/$', CompanyDetail.as_view(),
    	name="company_detail"),
    url(r'^company/(?P<slug>[-\w]+)/update/$', CompanyUpdate.as_view(),
    	name="company_update"),
    url(r'^company/(?P<slug>[-\w]+)/delete/$', CompanyDelete.as_view(),
    	name="company_delete"),
]