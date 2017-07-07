from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Employee(User):
	# """
 #    An abstract base class implementing a fully featured User model with
 #    admin-compliant permissions.

 #    Username and password are required. Other fields are optional.
 #    """
    is_warehouse = models.BooleanField(
        _('warehouse'),
        default=False,
        help_text=_(
            'Designates whether this staff member has warehouse permissions.'
        ),
    )
    is_financial = models.BooleanField(
        _('finance'),
        default=False,
        help_text=_(
            'Designates this staff member has financial permissions.'
        ),
    )
    is_service = models.BooleanField(
        _('service'),
        default=False,
        help_text=_(
            'Designates this staff member has services permissions.'
        ),
    )
    is_manager = models.BooleanField(
        _('manager'),
        default=False,
        help_text=_(
            'Designates this staff member has schedule and client permissions.'
        ),
    )
    is_maintenance = models.BooleanField(
        _('maintenance'),
        default=False,
        help_text=_(
            'Designates this staff member has maintenance permissions.'
        ),
    )

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.username