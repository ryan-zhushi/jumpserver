# -*- coding: utf-8 -*-

import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _

from orgs.mixins import OrgModelMixin


class System(OrgModelMixin):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=128, unique=True, verbose_name=_('Name'))
    homepage_url = models.URLField(max_length=128, unique=True, verbose_name=_('Homepage URL'))
    admin_url = models.URLField(max_length=256, blank=True, null=True, verbose_name=_('Admin URL'))
    admin_staff = models.CharField(max_length=128, verbose_name=_('Admin staff'))
    admin_staff_phone = models.CharField(max_length=20, verbose_name=_('Admin staff phone'))
    department = models.ForeignKey('systems.Department', blank=True, null=True, related_name='systems', verbose_name=_('Department'), on_delete=models.SET_NULL)
    created_by = models.CharField(max_length=30, blank=True, null=True, verbose_name=_('Created by'))
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=_('Date created'))
    date_updated = models.DateTimeField(auto_now=True, verbose_name=_('Date updated'))

    class Meta:
        verbose_name = _('System')

    def __str__(self):
        return self.name



