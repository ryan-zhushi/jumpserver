# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _

from orgs.mixins import OrgModelForm
from ..models import DomainName


class DomainNameForm(OrgModelForm):

    class Meta:
        model = DomainName
        fields = [
            'name', 'ip', 'type', 'comment'
        ]


class DomainNameBulkUpdateForm(OrgModelForm):

    class Meta:
        model = DomainName
        fields = [
            'name', 'ip', 'type', 'comment'
        ]

