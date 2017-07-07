from __future__ import unicode_literals

from django.conf.urls import url

from .views import (
	InvoiceListView, InvoiceCreateView, InvoiceDetailView, InvoiceUpdateView, 
	InvoiceDeleteView, AlterationDetailView, InvoicesConflictView,
	AlterationByInvoiceListView, AlterationCreateView, InvoicesOwedView
)


app_name = 'operation_finance'
urlpatterns = [
    url(r'^invoice_list/$', InvoiceListView.as_view(), 
    	name="invoice_list"),
    url(r'^invoice_owed_list/$', InvoicesOwedView.as_view(), 
    	name="invoice_owed_list"),
    url(r'^invoice_conflict_list/$', InvoicesConflictView.as_view(), 
    	name="invoice_conflict_list"),	
    url(r'^invoice/create/$', InvoiceCreateView.as_view(), 
    	name="invoice_create"),	
    url(r'^invoice/(?P<slug>[-\w]+)/$', InvoiceDetailView.as_view(), 
    	name="invoice_detail"),
    url(r'^invoice/(?P<slug>[-\w]+)/update/$', InvoiceUpdateView.as_view(), 
    	name="invoice_update"),
    url(r'^invoice/(?P<slug>[-\w]+)/delete/$', InvoiceDeleteView.as_view(), 
    	name="invoice_delete"),
    url(r'^alteration_list_by/([-\w]+)/$', AlterationByInvoiceListView.as_view(), 
    	name="alteration_by_invoice_list"),	
    url(r'^alteration/(?P<slug>[-\w]+)/create/$', AlterationCreateView.as_view(), 
    	name="alteration_create"),	
    url(r'^alteration/(?P<slug>[-\w]+)/$', AlterationDetailView.as_view(), 
    	name="alteration_detail"),
]
