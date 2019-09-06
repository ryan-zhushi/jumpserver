# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _

from orgs.mixins import OrgModelForm
from ..models import Department


class DepartmentForm(OrgModelForm):

    class Meta:
        model = Department
        fields = [
            'name', 'principal', 'principal_duty', 'principal_ecard',
            'principal_email', 'principal_phone', 'coordinator',
            'coordinator_duty', 'coordinator_ecard', 'coordinator_email',
            'coordinator_phone', 'coordinator_qq'
        ]


class DepartmentBulkUpdateForm(OrgModelForm):

    class Meta:
        model = Department
        fields = [
            'name', 'principal', 'principal_duty', 'principal_ecard',
            'principal_email', 'principal_phone', 'coordinator',
            'coordinator_duty', 'coordinator_ecard', 'coordinator_email',
            'coordinator_phone', 'coordinator_qq'
        ]

