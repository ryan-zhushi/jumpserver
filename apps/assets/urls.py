# coding:utf-8
from django.conf.urls import url, include
# from .api import (
#     AssetGroupViewSet, AssetViewSet, IDCViewSet
# )
import views
# from rest_framework import routers
# router = routers.DefaultRouter()
# router.register(r'assetgroup', AssetGroupViewSet)
# router.register(r'asset', AssetViewSet)
# router.register(r'idc', IDCViewSet)
app_name = 'assets'

urlpatterns = [
    # url(r'^$', views.AssetListView.as_view(), name='asset-index'),
    # url(r'^asset', views.AssetListView.as_view(), name='asset-list'),
    url(r'^asset/add$', views.AssetAddView.as_view(), name='asset-add'),
    url(r'^asset/(?P<pk>[0-9]+)$', views.AssetDetailView.as_view(), name='asset-detail'),
    url(r'^asset/(?P<pk>[0-9]+)$/edit', views.AssetEditView.as_view(), name='asset-edit'),
    url(r'^asset/(?P<pk>[0-9]+)/delete$', views.AssetDeleteView.as_view(), name='asset-delete'),
    url(r'^asset-group', views.AssetGroupListView.as_view(), name='asset-group-list'),
    url(r'^asset-group/add$', views.AssetGroupAddView.as_view(), name='asset-group-add'),
    url(r'^asset-group/(?P<pk>[0-9]+)$', views.AssetDetailView.as_view(), name='asset-group-detail'),
    url(r'^asset-group/(?P<pk>[0-9]+)$/edit', views.AssetEditView.as_view(), name='asset-group-edit'),
    url(r'^asset-group/(?P<pk>[0-9]+)/delete$', views.AssetDeleteView.as_view(), name='asset-group-delete'),
    # url(r'^api/v1.0/', include(router.urls)),
]