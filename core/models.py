from __future__ import unicode_literals

import uuid

from django.contrib.auth.models import User
from django.db import models


class Device(models.Model):
    customer = models.ForeignKey(User, null=True, blank=True)


class Task(models.Model):

    AVAILABLE = 1
    EXECUTING = 2
    COMPLETED = 3
    STATES_CHOICE = (
        (AVAILABLE, 'available'),
        (EXECUTING, 'executing'),
        (COMPLETED, 'completed'),
    )
    state = models.IntegerField(
        choices=STATES_CHOICE,
        default=AVAILABLE,
    )

    device = models.ForeignKey(Device, null=True, blank=True)

    owner = models.ForeignKey(User)

    def __str__(self):
        return 'id:%s state: %s' % (self.id, self.state)
