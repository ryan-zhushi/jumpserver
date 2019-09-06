from __future__ import absolute_import

from django.urls import path

from .. import views

app_name = 'systems'

urlpatterns = [
    path('system/', views.SystemListView.as_view(), name='system-list'),
    path('system/create/', views.SystemCreateView.as_view(), name='system-create'),
    path('system/<uuid:pk>/update/', views.SystemUpdateView.as_view(), name='system-update'),
    path('system/update/', views.SystemBulkUpdateView.as_view(), name='system-bulk-update'),
    path('system/<uuid:pk>/', views.SystemDetailView.as_view(), name='system-detail'),

    path('department/', views.DepartmentListView.as_view(), name='department-list'),
    path('department/create/', views.DepartmentCreateView.as_view(), name='department-create'),
    path('department/<uuid:pk>/update/', views.DepartmentUpdateView.as_view(), name='department-update'),
    path('department/update/', views.DepartmentBulkUpdateView.as_view(), name='department-bulk-update'),
    path('department/<uuid:pk>/', views.DepartmentDetailView.as_view(), name='department-detail'),
]
