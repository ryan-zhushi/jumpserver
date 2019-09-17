# -*- coding: utf-8 -*-

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.cache import cache
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import ugettext as _
from django.views.generic.base import TemplateView
from django.views.generic.edit import (
    CreateView, UpdateView
)
from django.views.generic.detail import DetailView

from common.const import (
    create_success_msg, update_success_msg, KEY_CACHE_RESOURCES_ID
)
from common.utils import get_logger
from common.permissions import (
    PermissionsMixin, IsOrgAdmin,
)
from orgs.utils import current_org
from .. import forms
from ..models import DomainName

__all__ = [
    'DomainNameListView', 'DomainNameCreateView', 'DomainNameDetailView',
    'DomainNameUpdateView', 'DomainNameBulkUpdateView',
]

logger = get_logger(__name__)


class DomainNameListView(PermissionsMixin, TemplateView):
    template_name = 'systems/domain_name_list.html'
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Systems'),
            'action': _('Domain name list'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class DomainNameCreateView(PermissionsMixin, SuccessMessageMixin, CreateView):
    model = DomainName
    form_class = forms.DomainNameForm
    template_name = 'systems/domain_name_create_update.html'
    success_url = reverse_lazy('domain-names:domain-name-list')
    success_message = create_success_msg
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Systems'),
            'action': _('Create domain name'),
            'type': 'create'
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        domain_name = form.save(commit=False)
        domain_name.created_by = self.request.user.username or 'DomainName'
        domain_name.save()
        return super().form_valid(form)


class DomainNameUpdateView(PermissionsMixin, SuccessMessageMixin, UpdateView):
    model = DomainName
    form_class = forms.DomainNameForm
    template_name = 'systems/domain_name_create_update.html'
    success_url = reverse_lazy('domain-names:domain-name-list')
    success_message = update_success_msg
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Systems'),
            'action': _('Update domain name'),
            'type': 'update'
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class DomainNameDetailView(PermissionsMixin, DetailView):
    model = DomainName
    context_object_name = 'domain_name'
    template_name = 'systems/domain_name_detail.html'
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Systems'),
            'action': _('Domain name detail'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class DomainNameBulkUpdateView(PermissionsMixin, TemplateView):
    model = DomainName
    form_class = forms.DomainNameBulkUpdateForm
    template_name = 'systems/domain_name_bulk_update.html'
    success_url = reverse_lazy('domain-names:domain-name-list')
    success_message = _("Bulk update domain_name success")
    form = None
    id_list = None
    permission_classes = [IsOrgAdmin]

    def get(self, request, *args, **kwargs):
        spm = request.GET.get('spm', '')
        domain_names_id = cache.get(KEY_CACHE_RESOURCES_ID.format(spm))
        if kwargs.get('form'):
            self.form = kwargs['form']
        elif domain_names_id:
            self.form = self.form_class(initial={'domain_names': domain_names_id})
        else:
            self.form = self.form_class()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, self.success_message)
            return redirect(self.success_url)
        else:
            return self.get(request, form=form, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {
            'app': 'Systems',
            'action': _('Bulk update domain name'),
            'form': self.form,
            'domain_names_selected': self.id_list,
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

