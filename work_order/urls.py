from __future__ import unicode_literals

from django.conf.urls import url
from django.contrib import admin

from .views import (
    OrderLists, OrderCreate, OrderDetail, OrderUpdate, OrderDelete,
    OrderAction
)


app_name = 'work_order'
urlpatterns = [
    
    url(r'^orders/([-\w]+)/$', OrderLists.as_view(), 
        name="order_list"),
    url(r'^order/add/$', OrderCreate.as_view(), 
        name="order_add"),  
    url(r'^order/(?P<slug>[-\w]+)/$', OrderDetail.as_view(), 
        name="order_detail"),
    url(r'^order/(?P<slug>[-\w]+)/update/$', OrderUpdate.as_view(), 
        name="order_update"),
    url(r'^order/(?P<slug>[-\w]+)/delete/$', OrderDelete.as_view(), 
        name="order_delete"),
    url(r'^order/(?P<slug>[-\w]+)/(?P<action>[-\w]+)/$', OrderAction.as_view(), 
        name="order_action"),
]
