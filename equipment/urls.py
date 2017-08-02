from __future__ import unicode_literals

from django.conf.urls import url

from .views import (
    BaseTypeList, BaseTypeCreate, BaseTypeUpdate, 
    BaseTypeDelete, JobToolCreate, JobToolDetail, JobToolUpdate, 
    JobToolDelete, JobToolCategoryList
)


app_name = 'equipment'
urlpatterns = [
    url(r'^base/$', BaseTypeList.as_view(), 
            name="base_list"),  
    url(r'^base/create/$', BaseTypeCreate.as_view(), 
            name="base_create"),    
    url(r'^base/(?P<slug>[-\w]+)/update/$', BaseTypeUpdate.as_view(), 
            name="base_update"),
    url(r'^base/(?P<slug>[-\w]+)/delete/$', BaseTypeDelete.as_view(), 
            name="base_delete"),
    url(r'^job_tool/(?P<slug>[-\w]+)/create/$', JobToolCreate.as_view(), 
            name="job_tool_create"),    
    url(r'^job_tool/(?P<slug>[-\w]+)/$', JobToolDetail.as_view(), 
            name="job_tool_detail"),
    url(r'^job_tool/(?P<slug>[-\w]+)/update/$', JobToolUpdate.as_view(), 
            name="job_tool_update"),
    url(r'^job_tool/(?P<slug>[-\w]+)/delete/$', JobToolDelete.as_view(), 
            name="job_tool_delete"),
    url(r'^category_job_tool/([\w-]+)/$', JobToolCategoryList.as_view(), 
            name="job_tool_and_category_list"),     
]