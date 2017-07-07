from __future__ import unicode_literals

from django.db import models
import datetime
from datetime import datetime
import time

from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
# from employee.models import Employee
from source_utils.starters import CommonInfo


DAYS_OF_WEEK = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    )


class DayStaffLogBase(CommonInfo):
    start = models.TimeField(_("start"))
    end = models.TimeField(_("end"))
    actual_start = models.TimeField(_("actual start"))
    actual_end = models.TimeField(_("actual end"))

    class Meta:
        abstract = True


class DayLog(models.Model):
    """ 
    This model represents . 
    """

    slug = models.SlugField(blank=True)
    day = models.DateField(unique=True)

    def __str__(self):
        return str(self.day)

def pre_save_day_log(sender, instance, *args, **kwargs):

    instance.slug = slugify(instance.day)

pre_save.connect(pre_save_day_log, sender=DayLog)


class DayStaffLogDetails(DayStaffLogBase):
    day = models.ForeignKey(
        DayLog, 
        on_delete=models.CASCADE, 
        verbose_name=_("day for log")
    )
    # staff = models.ForeignKey(
    #     Employee, 
    #     limit_choices_to={
    #         'is_active': True
    #     }, 
    #     on_delete=models.CASCADE, 
    #     verbose_name=_("Staff Member")
    # )
    hole = models.BooleanField(
        _("schedule hole"), 
        default=False
    )
    full = models.BooleanField(
        _("full"),
        default=False
    )
    over_time = models.BooleanField(
        _("over time"),
        default=False
    )

    class Meta:
        verbose_name = _("Staff's Overall Time For Day")
        verbose_name_plural = _("Staff's Overall Times For Day")
        # ordering = ["staff", "day"]
        # unique_together = ("day", "staff")

    # def __str__(self):
    #     return "{} - {}".format(self.day.__str__(), self.staff.get_full_name())

    # def get_absolute_url(self):
    #     return reverse("time_log:staff_log_detail", kwargs={'slug': self.slug})


# def pre_save_staff_time_log(sender, instance, *args, **kwargs):
#     slug = "{}/{}".format(instance.staff.slug, instance.day.slug)
#     instance.slug = slugify(slug)

# pre_save.connect(pre_save_staff_time_log, sender=DayStaffLogDetails)


class DayStaffLogEntry(DayStaffLogBase):
    day = models.ForeignKey(
        DayStaffLogDetails, 
        on_delete=models.CASCADE, 
        verbose_name=_("day log for entry")
    )
    slug_for_item = models.SlugField(blank=True)
    reference = models.CharField(_("reference"), max_length=30)
    note = models.CharField(_("note"), max_length=300)
    complete = models.BooleanField(
        _("complete"),
        default=False
    )
    cancelled = models.BooleanField(
        _("cancelled"),
        default=False
    )

    class Meta:
        verbose_name = _("Staff's Item Entry For Day Log")
        verbose_name_plural = _("Staff's Item Entries For Day Log")
        ordering = ["day", "start"]

    # def __str__(self):
    #     return "{} - {}".format(self.day.__str__(), self.staff.get_full_name())

    # def get_absolute_url(self):
    #     return reverse("time_log:staff_log_detail", kwargs={'slug': self.slug})


def pre_save_staff_time_log(sender, instance, *args, **kwargs):
    start_date = str(instance.start)
    start_date = start_date[:10]
    try:
        find_start_date = DayLog.objects.get(day=start_date)
    except DayLog.DoesNotExist:
        find_start_date = DayLog(day=start_date)
        find_start_date.save()
    slug = "{}/{}/{}".format(instance.day.slug, instance.reference, instance.pk)
    instance.slug = slugify(slug)

pre_save.connect(pre_save_staff_time_log, sender=DayStaffLogEntry)


class StaffLog(CommonInfo):
    """ 
    This model represents t. 
    """
    # staff = models.ForeignKey(
    #     Employee, 
    #     limit_choices_to={
    #         'is_active': True
    #     }, 
    #     on_delete=models.CASCADE, 
    #     verbose_name=_("Staff Member")
    # )
    day = models.CharField(
        _('Day of the week'),
        max_length=12, 
        choices=DAYS_OF_WEEK
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
        # ordering = ["staff"]
        # unique_together = ("staff", "day")

    def convert_time(self, time):
        reformatted_time = datetime.strptime(str(time), "%H:%M:%S")
        return reformatted_time.strftime("%I:%M %p")


    def __str__(self):
        return "{}: {} to {}".format(
            self.day, 
            self.convert_time(self.scheduled_start), 
            self.convert_time(self.scheduled_end)
        )

    # def get_absolute_url(self):
    #     return reverse("time_log:staff_log_detail", kwargs={'slug': self.slug})

    # def get_url(self):
    #     return reverse('time_log:staff_log_list', kwargs = {'pk' : self.staff.pk})


# def pre_save_staff_time_log(sender, instance, *args, **kwargs):
#     slug = "{} {}".format(instance.staff.get_full_name(), instance.day)
#     instance.slug = slugify(slug)

# pre_save.connect(pre_save_staff_time_log, sender=StaffLog)
