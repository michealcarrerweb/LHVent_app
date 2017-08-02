from __future__ import unicode_literals

from django.contrib import admin

from .models import (
	AvailabilityForDay, LoggedDay, StaffLogDetailsForDay, GenericActivity,
	ScheduledTimeSlotEntry
)


admin.site.register(AvailabilityForDay)
admin.site.register(LoggedDay)
admin.site.register(StaffLogDetailsForDay)
admin.site.register(GenericActivity)
admin.site.register(ScheduledTimeSlotEntry)
