from __future__ import unicode_literals

from django.conf.urls import url
from django.contrib import admin

from .views import (
	BaseTypeList, BaseTypeCreate, BaseTypeDetail, BaseTypeUpdate, 
	BaseTypeDelete, ItemDetail, ItemList, ItemCreate, ItemUpdate, 
    ItemDelete, ItemCategoryList, ImageUpdate, ImageDetail, ItemSupplierList, 
    SupplierItemCreate, BaseItemCreate, ItemAddDamaged, ItemAdd
)


app_name = 'product'
urlpatterns = [
    # Product Categories
    url(r'^base/$', BaseTypeList.as_view(),
    	name="base_product_list"),	
    url(r'^base/create/$', BaseTypeCreate.as_view(),
    	name="base_product_create"),
    url(r'^base/(?P<slug>[-\w]+)/$', BaseTypeDetail.as_view(),
    	name="base_product_detail"),
    url(r'^base/(?P<slug>[-\w]+)/update/$', BaseTypeUpdate.as_view(),
    	name="base_product_update"),
    url(r'^base/(?P<slug>[-\w]+)/delete/$', BaseTypeDelete.as_view(),
    	name="base_product_delete"),
    # Products
    url(r'^item/$', ItemList.as_view(),
    	name="item_list"),
    url(r'^item/create/$', ItemCreate.as_view(),
    	name="item_create"),	
    url(r'^item/create/supplier/([\w-]+)/$', SupplierItemCreate.as_view(),
    	name="supplier_item_create"),
    url(r'^item/create/base/([\w-]+)/$', BaseItemCreate.as_view(),
    	name="base_item_create"),
    url(r'^item/(?P<slug>[-\w]+)/$', ItemDetail.as_view(),
    	name="item_detail"),
    url(r'^item/(?P<slug>[-\w]+)/update/$', ItemUpdate.as_view(),
    	name="item_update"),
    url(r'^item/(?P<slug>[-\w]+)/delete/$', ItemDelete.as_view(),
    	name="item_delete"),
    url(r'^item/([-\w]+)/add_damaged/$', ItemAddDamaged.as_view(),
    	name="item_add_damaged"),
    url(r'^item/([-\w]+)/add/$', ItemAdd.as_view(),
    	name="item_add"),
    # Product Images
    url(r'^image_for_item/(?P<slug>[-\w]+)/update/$', ImageUpdate.as_view(),
    	name="image_update"),
    url(r'^image/(?P<slug>[-\w]+)/$', ImageDetail.as_view(),
    	name="image_detail"),
    # Products by Categories
    url(r'^category_items/([\w-]+)/$', ItemCategoryList.as_view(),
    	name="category_item_list"),
    # Product by Supplier
    url(r'^supplier_items/([\w-]+)/$', ItemSupplierList.as_view(),
    	name="supplier_item_list"),
]