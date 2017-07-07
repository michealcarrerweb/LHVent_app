from __future__ import unicode_literals

from django.contrib import admin

from .models import Invoice, InvoiceAlteration


admin.site.register(Invoice)
admin.site.register(InvoiceAlteration)
