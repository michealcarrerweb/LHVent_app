from __future__ import unicode_literals

from django.conf.urls import url

from .views import (
	PricingCreateView, PricingListView, PricingUpdateView, 
	PricingDetailView, HourlyBaseUpdateView, 
	MainLedgerDetailView
)

app_name = 'finance'
urlpatterns = [
	url(r'^pricing_list/$', PricingListView.as_view(), 
		name="pricing_list"),
	url(r'^hourly_base/(?P<pk>[1])/change/$', HourlyBaseUpdateView.as_view(), 
		name="hourly_base_update"),
	url(r'^pricing/create/$', PricingCreateView.as_view(), 
		name="pricing_create"),
	url(r'^pricing/(?P<slug>[-\w]+)/$', PricingDetailView.as_view(), 
			name="pricing_detail"),
	url(r'^pricing/(?P<slug>[-\w]+)/update/$', PricingUpdateView.as_view(), 
		name="pricing_update"),

	url(r'^parent_ledger/(?P<pk>[1])/$', MainLedgerDetailView.as_view(), 
			name="main_ledger_detail"),
]
