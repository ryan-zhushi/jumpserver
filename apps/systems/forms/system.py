# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _

from orgs.mixins import OrgModelForm
from ..models import System


class SystemForm(OrgModelForm):

    class Meta:
        model = System
        fields = [
            'name', 'homepage_url', 'admin_url', 'admin_staff',
            'admin_staff_phone', 'department',
        ]


class SystemBulkUpdateForm(OrgModelForm):

    class Meta:
        model = System
        fields = ['name', 'admin_staff', 'admin_staff_phone', 'department']
