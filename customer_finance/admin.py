from __future__ import unicode_literals

from django.contrib import admin

from .models import Invoice, InvoiceAlteration, CustomerConflict, PriceQuote


admin.site.register(Invoice)
admin.site.register(InvoiceAlteration)
admin.site.register(CustomerConflict)
admin.site.register(PriceQuote)