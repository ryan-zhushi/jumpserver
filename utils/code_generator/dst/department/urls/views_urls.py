from __future__ import absolute_import

from django.urls import path

from .. import views

app_name = 'departments'

urlpatterns = [
    path('department/', views.DepartmentListView.as_view(), name='department-list'),
    path('department/create/', views.DepartmentCreateView.as_view(), name='department-create'),
    path('department/<uuid:pk>/update/', views.DepartmentUpdateView.as_view(), name='department-update'),
    path('department/update/', views.DepartmentBulkUpdateView.as_view(), name='department-bulk-update'),
    path('department/<uuid:pk>/', views.DepartmentDetailView.as_view(), name='department-detail'),
]
