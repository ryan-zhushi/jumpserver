# -*- coding: utf-8 -*-

import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _

from orgs.mixins import OrgModelMixin


class Department(OrgModelMixin):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=128, unique=True, verbose_name=_('Name'))
    principal = models.CharField(max_length=128, verbose_name=_('Principal'))
    principal_duty = models.CharField(max_length=128, verbose_name=_('Principal duty'))
    principal_ecard = models.CharField(max_length=128, unique=True, verbose_name=_('Principal ecard'))
    principal_email = models.EmailField(max_length=128, unique=True, verbose_name=_('Principal Email'))
    principal_phone = models.CharField(max_length=20, verbose_name=_('Principal phone'))
    coordinator = models.CharField(max_length=128, verbose_name=_('Coordinator'))
    coordinator_duty = models.CharField(max_length=128, verbose_name=_('Coordinator duty'))
    coordinator_ecard = models.CharField(max_length=128, unique=True, verbose_name=_('Coordinator ecard'))
    coordinator_email = models.EmailField(max_length=128, unique=True, verbose_name=_('Coordinator Email'))
    coordinator_phone = models.CharField(max_length=20, verbose_name=_('Coordinator phone'))
    coordinator_qq = models.CharField(max_length=128, verbose_name=_('Coordinator qq'))
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=('Date created'))

    class Meta:
        verbose_name = _('Department')

    def __str__(self):
        return self.name

