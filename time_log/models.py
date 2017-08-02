from __future__ import unicode_literals

from django.db import models
import datetime
from datetime import datetime
import time

from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from source_utils.starters import CommonInfo
from work_order.models import Order


DAYS_OF_WEEK = [
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
    ('Sunday', 'Sunday'),
]


class LoggedDay(models.Model):
    """ 
    This model represents . 
    """

    slug = models.SlugField(blank=True)
    day = models.DateField(unique=True)

    def __str__(self):
        return str(self.day)

    def calculate_hours_for_day(self):
        pass
        # day_str = self.day.strftime("%A")
        # staff_avail_for_day = AvailabilityForDay.objects.filter(day=day_str)
        # total_staff_hrs_for_day = 0
        # for item in staff_avail_for_day:
        #     total_staff_hrs_for_day += item.calculate_hours()
        # return total_staff_hrs_for_day


def pre_save_logged_day(sender, instance, *args, **kwargs):

    instance.slug = slugify(instance.day)

pre_save.connect(pre_save_logged_day, sender=LoggedDay)


class StaffLogDetailsForDay(CommonInfo):
    day = models.ForeignKey(
        LoggedDay, 
        on_delete=models.CASCADE,
        related_name="daylogdetail", 
        verbose_name=_("Day for log")
    )
    staff = models.ForeignKey(
        User, 
        limit_choices_to={
            'is_active': True,
            'is_staff':True
        },
        related_name="staffday", 
        on_delete=models.CASCADE, 
        verbose_name=_("Staff Member")
    )

    class Meta:
        verbose_name = _("Staff's Overall Time For Day")
        verbose_name_plural = _("Staff's Overall Times For Day")
        ordering = ["staff", "day"]
        unique_together = ("day", "staff")

    def __str__(self):
        return "{} - {}".format(self.day.__str__(), self.staff.username)

    # def get_absolute_url(self):
    #     return reverse("time_log:staff_log_detail", kwargs={'slug': self.slug})


def pre_save_staff_log_details_for_day(sender, instance, *args, **kwargs):
    slug = "{}/{}".format(instance.staff.__str__(), instance.day.slug)
    instance.slug = slugify(slug)

pre_save.connect(pre_save_staff_log_details_for_day, sender=StaffLogDetailsForDay)


class GenericActivity(models.Model):
    """ 
    This model represents the general type of service category offered. 
    """

    slug = models.SlugField(blank=True)
    activity = models.CharField(_("activity"), max_length=50)

    class Meta:
        verbose_name = _('Activity Type')
        verbose_name_plural = _('Activity Types')
        ordering = ["activity"]

    def __str__(self):
        return str(self.activity)

    # def get_success_url(self):
    #     return reverse(
    #         "time_log:activity_list"
    #         )

    # def get_absolute_url(self):
    #     return reverse(
    #         "time_log:activity_detail", 
    #         kwargs={'slug': self.slug}
    #         )

def pre_save_generic_activity(sender, instance, *args, **kwargs):
    instance.slug = slugify(instance.activity)

pre_save.connect(pre_save_generic_activity, sender=GenericActivity)


class ScheduledTimeSlotEntry(models.Model):

    staff_day = models.ForeignKey(
        StaffLogDetailsForDay,  
        on_delete=models.CASCADE,
        related_name='staffslot', 
        verbose_name=_("Staff Day")
    )
    activity = models.ForeignKey(
        GenericActivity, 
        on_delete=models.CASCADE,
        related_name='slotactivity', 
        verbose_name=_("activity")
    )
    work_order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE,
        related_name='workorder',
        blank=True,
        null=True, 
        verbose_name=_("work order")
    )
    start = models.TimeField(_("scheduled start"))
    end = models.TimeField(_("scheduled end"))
    firm = models.BooleanField(
        _("firm schedule"),
        default=False
    )  

    class Meta:
        verbose_name = _("Scheduled Time Slot")
        verbose_name_plural = _("Scheduled Time Slots")
        ordering = ["work_order",]

    def __str__(self):
        return "{} - {} - {}".format(
            self.staff_day.__str__(), 
            self.activity.__str__(), 
            self.work_order.__str__()
        )

    # def save(self, *args, **kwargs):
    #     super(ScheduledTimeSlotEntry, self).save(*args, **kwargs)
    #     if self.staff_day.scheduled_start:
    #         self.staff_day.scheduled_end = self.end
    #     else:
    #         self.staff_day.scheduled_start = self.start
    #         self.staff_day.scheduled_end = self.end
    #     self.staff_day.save()

# def pre_save_staff_time_log(sender, instance, *args, **kwargs):
#     start_date = str(instance.start)
#     start_date = start_date[:10]
#     try:
#         find_start_date = DayLog.objects.get(day=start_date)
#     except DayLog.DoesNotExist:
#         find_start_date = DayLog(day=start_date)
#         find_start_date.save()
#     slug = "{}/{}/{}".format(instance.day.slug, instance.reference, instance.pk)
#     instance.slug = slugify(slug)


class AvailabilityForDay(CommonInfo):
    """ 
    This model represents t. 
    """
    staff = models.ForeignKey(
        User, 
        limit_choices_to={
            'is_active': True,
            'is_staff':True
        }, 
        on_delete=models.CASCADE,
        related_name='employee', 
        verbose_name=_("Staff Member")
    )
    day = models.CharField(
        _('Day of the week'),
        max_length=12 
    )
    scheduled_start = models.TimeField(
        _("start time of day"),
        default="07:00" 
    )
    scheduled_end = models.TimeField(
        _("end time of day"), 
        default="17:00"
    )
  
    class Meta:
        verbose_name = _("Staff's Scheduled Hours For Day Of The Week")
        verbose_name_plural = _("Staff's Scheduled Hours For Days Of The Week")
        ordering = ["staff", "day"]
        unique_together = ("staff", "day")

    def convert_time(self, time):
        reformatted_time = datetime.strptime(str(time), "%H:%M:%S")
        return reformatted_time.strftime("%I:%M %p")

    def calculate_hours(self):
        print(self.scheduled_start)
        # return self.scheduled_end - self.scheduled_start

    def __str__(self):
        return "{} - {}: {} to {}".format(
            self.staff,
            self.day, 
            self.convert_time(self.scheduled_start), 
            self.convert_time(self.scheduled_end)
        )

    def get_absolute_url(self):
        return reverse('time_log:staff_avail_update', kwargs = {'pk' : self.pk})


def pre_save_staff_avail_for_day(sender, instance, *args, **kwargs):
    slug = "{} {}".format(instance.staff.username, instance.day)
    instance.slug = slugify(slug)

pre_save.connect(pre_save_staff_avail_for_day, sender=AvailabilityForDay)


    # scheduled_start = models.TimeField(
    #     _("actual start"),
    #     blank=True, 
    #     null=True
    # )
    # scheduled_end = models.TimeField(
    #     _("actual start"),
    #     blank=True, 
    #     null=True
    # )
    # actual_start = models.TimeField(
    #     _("actual start"),
    #     blank=True, 
    #     null=True
    # )
    # actual_end = models.TimeField(
    #     _("actual end"),
    #     blank=True, 
    #     null=True
    # )
    # forecasted_hours_for_day = models.DecimalField(
    #     max_digits=5, 
    #     decimal_places=3,
    #     blank=True, 
    #     null=True
    # )
    # actual_hours_for_day = models.DecimalField(
    #     max_digits=5, 
    #     decimal_places=3,
    #     blank=True, 
    #     null=True
    # )
    # full = models.BooleanField(
    #     _("full"),
    #     default=False
    # )
    # over_time = models.BooleanField(
    #     _("over time"),
    #     default=False
    # )