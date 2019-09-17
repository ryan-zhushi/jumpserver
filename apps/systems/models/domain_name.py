# -*- coding: utf-8 -*-

import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _

from orgs.mixins import OrgModelMixin


class DomainName(OrgModelMixin):
    TYPE_CHOICES = (
        ('A', 'normal ex: zb IN A 202.195.160.31'),
        ('asp2', '78_ASP server'),
        ('wwwsub', 'PHP server'),
        ('rproxy', 'Reverse proxy'),
        ('httpsvr', 'httpsvr'),
        ('asp3', '73_ASP server'),
        ('wzq', 'WZQ server'),
        ('a10jiaoyuwang', 'A10 jiaoyuwang proxy'),
        ('a10xiaonei', 'A10 jiaoyuwang proxy'),
    )

    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=128, blank=True, null=True, verbose_name=_('Domain name'))
    ip = models.CharField(max_length=128, blank=True, null=True, verbose_name=_('IP'))
    type = models.CharField(max_length=128, choices=TYPE_CHOICES, default='A', verbose_name=_('Type'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is active'))
    comment = models.CharField(max_length=128, blank=True, null=True, verbose_name=_('Comment'))
    created_by = models.CharField(max_length=30, blank=True, null=True, verbose_name=_('Created by'))
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=_('Date created'))
    date_updated = models.DateTimeField(auto_now=True, verbose_name=_('Date updated'))

    class Meta:
        verbose_name = _('Domain name')

    def __str__(self):
        return self.name

