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
    PermissionsMixin, IsOrgAdmin, IsValidUser,
)
from orgs.utils import current_org
from .. import forms
from ..models import System

__all__ = [
    'SystemListView', 'SystemCreateView', 'SystemDetailView',
    'SystemUpdateView', 'SystemBulkUpdateView',
]

logger = get_logger(__name__)


class SystemListView(PermissionsMixin, TemplateView):
    template_name = 'systems/system_list.html'
    permission_classes = [IsValidUser]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Systems'),
            'action': _('System list'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class SystemCreateView(PermissionsMixin, SuccessMessageMixin, CreateView):
    model = System
    form_class = forms.SystemForm
    template_name = 'systems/system_create_update.html'
    success_url = reverse_lazy('systems:system-list')
    success_message = create_success_msg
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Systems'),
            'action': _('Create system'),
            'type': 'create'
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        system = form.save(commit=False)
        system.created_by = self.request.user.username or 'System'
        system.save()
        return super().form_valid(form)


class SystemUpdateView(PermissionsMixin, SuccessMessageMixin, UpdateView):
    model = System
    form_class = forms.SystemForm
    template_name = 'systems/system_create_update.html'
    success_url = reverse_lazy('systems:system-list')
    success_message = update_success_msg
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Systems'),
            'action': _('Update system'),
            'type': 'update'
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class SystemDetailView(PermissionsMixin, DetailView):
    model = System
    context_object_name = 'system'
    template_name = 'systems/system_detail.html'
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Systems'),
            'action': _('System detail'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class SystemBulkUpdateView(PermissionsMixin, TemplateView):
    model = System
    form_class = forms.SystemBulkUpdateForm
    template_name = 'systems/system_bulk_update.html'
    success_url = reverse_lazy('systems:system-list')
    success_message = _("Bulk update system success")
    form = None
    id_list = None
    permission_classes = [IsOrgAdmin]

    def get(self, request, *args, **kwargs):
        spm = request.GET.get('spm', '')
        systems_id = cache.get(KEY_CACHE_RESOURCES_ID.format(spm))
        if kwargs.get('form'):
            self.form = kwargs['form']
        elif systems_id:
            self.form = self.form_class(initial={'systems': systems_id})
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
            'action': _('Bulk update system'),
            'form': self.form,
            'systems_selected': self.id_list,
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)