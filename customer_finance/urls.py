from __future__ import unicode_literals

from django.conf.urls import url

from .views import (
    InvoiceCreateView, InvoiceDetailView, InvoiceUpdateView, 
	InvoiceDeleteView, AlterationDetailView, AlterationByInvoiceListView, 
    AlterationCreateView, print_users, InvoiceGiveQuoteView, 
    CustomerConflictCreateView, CustomerConflictUpdateView, 
    CustomerConflictResolveView, InvoicesOptionsListView, InvoiceCloseOutView
)


app_name = 'customer_finance'
urlpatterns = [
    url(r'^invoice_list/([-\w]+)/$', InvoicesOptionsListView.as_view(), 
        name="invoice_lists"),
    url(r'^invoice/create/$', InvoiceCreateView.as_view(), 
    	name="invoice_create"),	
    url(r'^invoice/(?P<slug>[-\w]+)/$', InvoiceDetailView.as_view(), 
    	name="invoice_detail"),
    url(r'^invoice/(?P<slug>[-\w]+)/update/$', InvoiceUpdateView.as_view(), 
    	name="invoice_update"),
    url(r'^invoice/(?P<slug>[-\w]+)/quote/$', InvoiceGiveQuoteView.as_view(), 
        name="invoice_give_quote"),
    url(r'^invoice/(?P<slug>[-\w]+)/close_out/$', InvoiceCloseOutView.as_view(), 
        name="close_out"),
    url(r'^invoice/(?P<slug>[-\w]+)/delete/$', InvoiceDeleteView.as_view(), 
    	name="invoice_delete"),
    url(r'^alteration_list_by/(?P<slug>[-\w]+)/$', AlterationByInvoiceListView.as_view(), 
    	name="alteration_by_invoice_list"),	
    url(r'^alteration/(?P<slug>[-\w]+)/create/$', AlterationCreateView.as_view(), 
    	name="alteration_create"),	
    url(r'^alteration/(?P<pk>\d+)/$', AlterationDetailView.as_view(), 
    	name="alteration_detail"),
    url(r'^conflict/(?P<slug>[-\w]+)/create/$', CustomerConflictCreateView.as_view(), 
        name="conflict_create"),
    url(r'^conflict/(?P<pk>\d+)/update/$', CustomerConflictUpdateView.as_view(), 
        name="conflict_update"),
    url(r'^conflict/(?P<pk>\d+)/resolve/$', CustomerConflictResolveView.as_view(), 
        name="conflict_resolve"),
    url(r'^invoice/(?P<slug>[-\w]+)/pdf/$', print_users, 
    	name="invoice_pdf"),
]
