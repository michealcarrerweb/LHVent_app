from __future__ import unicode_literals

from django.contrib import admin

from .models import (DayLog, StaffLog, DayStaffLogDetails, DayStaffLogEntry)


admin.site.register(DayLog)
admin.site.register(StaffLog)
admin.site.register(DayStaffLogDetails)
admin.site.register(DayStaffLogEntry)