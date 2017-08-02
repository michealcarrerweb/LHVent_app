from __future__ import unicode_literals

from django.contrib import admin


from .models import Base, Product


admin.site.register(Base)
admin.site.register(Product)
