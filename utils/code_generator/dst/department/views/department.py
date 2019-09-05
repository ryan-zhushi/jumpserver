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
from ..models import Department

__all__ = [
    'DepartmentListView', 'DepartmentCreateView', 'DepartmentDetailView',
    'DepartmentUpdateView', 'DepartmentBulkUpdateView',
]

logger = get_logger(__name__)


class DepartmentListView(PermissionsMixin, TemplateView):
    template_name = 'departments/department_list.html'
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Departments'),
            'action': _('Department list'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class DepartmentCreateView(PermissionsMixin, SuccessMessageMixin, CreateView):
    model = Department
    form_class = forms.DepartmentForm
    template_name = 'departments/department_create_update.html'
    success_url = reverse_lazy('departments:department-list')
    success_message = create_success_msg
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Departments'),
            'action': _('Create department'),
            'type': 'create'
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        department = form.save(commit=False)
        department.created_by = self.request.user.username or 'Department'
        department.save()
        return super().form_valid(form)


class DepartmentUpdateView(PermissionsMixin, SuccessMessageMixin, UpdateView):
    model = Department
    form_class = forms.DepartmentForm
    template_name = 'departments/department_create_update.html'
    success_url = reverse_lazy('departments:department-list')
    success_message = update_success_msg
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Departments'),
            'action': _('Update department'),
            'type': 'update'
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class DepartmentDetailView(PermissionsMixin, DetailView):
    model = Department
    context_object_name = 'department'
    template_name = 'departments/department_detail.html'
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Departments'),
            'action': _('Department detail'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class DepartmentBulkUpdateView(PermissionsMixin, TemplateView):
    model = Department
    form_class = forms.DepartmentBulkUpdateForm
    template_name = 'departments/department_bulk_update.html'
    success_url = reverse_lazy('departments:department-list')
    success_message = _("Bulk update department success")
    form = None
    id_list = None
    permission_classes = [IsOrgAdmin]

    def get(self, request, *args, **kwargs):
        spm = request.GET.get('spm', '')
        departments_id = cache.get(KEY_CACHE_RESOURCES_ID.format(spm))
        if kwargs.get('form'):
            self.form = kwargs['form']
        elif departments_id:
            self.form = self.form_class(initial={'departments': departments_id})
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
            'app': 'Departments',
            'action': _('Bulk update department'),
            'form': self.form,
            'departments_selected': self.id_list,
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)
