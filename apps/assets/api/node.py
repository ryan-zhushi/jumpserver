# ~*~ coding: utf-8 ~*~
# Copyright (C) 2014-2018 Beijing DuiZhan Technology Co.,Ltd. All Rights Reserved.
#
# Licensed under the GNU General Public License v2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.gnu.org/licenses/gpl-2.0.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import time

from rest_framework import generics, mixins, viewsets
from rest_framework.serializers import ValidationError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404

from common.utils import get_logger, get_object_or_none
from common.tree import TreeNodeSerializer
from orgs.mixins.api import OrgModelViewSet
from ..hands import IsOrgAdmin
from ..models import Node
from ..tasks import update_assets_hardware_info_util, test_asset_connectivity_util
from .. import serializers
from ..utils import NodeUtil


logger = get_logger(__file__)
__all__ = [
    'NodeViewSet', 'NodeChildrenApi', 'NodeAssetsApi',
    'NodeAddAssetsApi', 'NodeRemoveAssetsApi', 'NodeReplaceAssetsApi',
    'NodeAddChildrenApi', 'RefreshNodeHardwareInfoApi',
    'TestNodeConnectiveApi', 'NodeListAsTreeApi',
    'NodeChildrenAsTreeApi', 'RefreshAssetsAmount',
]


class NodeViewSet(OrgModelViewSet):
    filter_fields = ('value', 'key', 'id')
    search_fields = ('value', )
    queryset = Node.objects.all()
    permission_classes = (IsOrgAdmin,)
    serializer_class = serializers.NodeSerializer
    pagination_class = LimitOffsetPagination

    # 仅支持根节点指直接创建，子节点下的节点需要通过children接口创建
    def perform_create(self, serializer):
        child_key = Node.root().get_next_child_key()
        serializer.validated_data["key"] = child_key
        serializer.save()

    def perform_update(self, serializer):
        node = self.get_object()
        if node.is_root() and node.value != serializer.validated_data['value']:
            msg = _("You can't update the root node name")
            raise ValidationError({"error": msg})
        return super().perform_update(serializer)


class NodeListAsTreeApi(generics.ListAPIView):
    """
    获取节点列表树
    [
      {
        "id": "",
        "name": "",
        "pId": "",
        "meta": ""
      }
    ]
    """
    permission_classes = (IsOrgAdmin,)
    serializer_class = TreeNodeSerializer

    def to_tree_queryset(self, queryset):
        util = NodeUtil()
        nodes = util.get_nodes_by_queryset(queryset)
        queryset = [node.as_tree_node() for node in nodes]
        return queryset

    def get_queryset(self):
        queryset = Node.objects.all()
        return queryset

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        queryset = self.to_tree_queryset(queryset)
        return queryset


class NodeChildrenApi(mixins.ListModelMixin, generics.CreateAPIView):
    queryset = Node.objects.all()
    permission_classes = (IsOrgAdmin,)
    serializer_class = serializers.NodeSerializer
    instance = None

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        if not request.data.get("value"):
            request.data["value"] = instance.get_next_child_preset_name()
        return super().post(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        instance = self.get_object()
        value = request.data.get("value")
        _id = request.data.get('id') or None
        values = [child.value for child in instance.get_children()]
        if value in values:
            raise ValidationError(
                'The same level node name cannot be the same'
            )
        node = instance.create_child(value=value, _id=_id)
        return Response(self.serializer_class(instance=node).data, status=201)

    def get_object(self):
        pk = self.kwargs.get('pk') or self.request.query_params.get('id')
        if not pk:
            node = Node.root()
        else:
            node = get_object_or_404(Node, pk=pk)
        return node

    def get_queryset(self):
        queryset = []
        query_all = self.request.query_params.get("all")
        node = self.get_object()

        if node is None:
            node = Node.root()
            node.assets__count = node.get_all_assets().count()
            queryset.append(node)

        if query_all:
            children = node.get_all_children()
        else:
            children = node.get_children()
        queryset.extend(list(children))
        return queryset


class NodeChildrenAsTreeApi(generics.ListAPIView):
    """
    节点子节点作为树返回，
    [
      {
        "id": "",
        "name": "",
        "pId": "",
        "meta": ""
      }
    ]

    """
    permission_classes = (IsOrgAdmin,)
    serializer_class = TreeNodeSerializer
    node = None
    is_root = False

    def get_queryset(self):
        self.check_need_refresh_nodes()
        node_key = self.request.query_params.get('key')
        # 是否包含自己
        with_self = False
        if not node_key:
            node_key = Node.root().key
            with_self = True
        self.node = get_object_or_404(Node, key=node_key)
        queryset = self.node.get_children(with_self=with_self)
        queryset = [node.as_tree_node() for node in queryset]
        queryset = sorted(queryset)
        return queryset

    def filter_assets(self, queryset):
        include_assets = self.request.query_params.get('assets', '0') == '1'
        if not include_assets:
            return queryset
        assets = self.node.get_assets().only(
            "id", "hostname", "ip", 'platform', "os",
            "org_id", "protocols",
        )
        for asset in assets:
            queryset.append(asset.as_tree_node(self.node))
        return queryset

    def filter_queryset(self, queryset):
        queryset = self.filter_assets(queryset)
        return queryset

    def check_need_refresh_nodes(self):
        if self.request.query_params.get('refresh', '0') == '1':
            Node.refresh_nodes()


class NodeAssetsApi(generics.ListAPIView):
    permission_classes = (IsOrgAdmin,)
    serializer_class = serializers.AssetSerializer

    def get_queryset(self):
        node_id = self.kwargs.get('pk')
        query_all = self.request.query_params.get('all')
        instance = get_object_or_404(Node, pk=node_id)
        if query_all:
            return instance.get_all_assets()
        else:
            return instance.get_assets()


class NodeAddChildrenApi(generics.UpdateAPIView):
    queryset = Node.objects.all()
    permission_classes = (IsOrgAdmin,)
    serializer_class = serializers.NodeAddChildrenSerializer
    instance = None

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        nodes_id = request.data.get("nodes")
        children = [get_object_or_none(Node, id=pk) for pk in nodes_id]
        for node in children:
            if not node:
                continue
            node.parent = instance
        return Response("OK")


class NodeAddAssetsApi(generics.UpdateAPIView):
    serializer_class = serializers.NodeAssetsSerializer
    queryset = Node.objects.all()
    permission_classes = (IsOrgAdmin,)
    instance = None

    def perform_update(self, serializer):
        assets = serializer.validated_data.get('assets')
        instance = self.get_object()
        instance.assets.add(*tuple(assets))


class NodeRemoveAssetsApi(generics.UpdateAPIView):
    serializer_class = serializers.NodeAssetsSerializer
    queryset = Node.objects.all()
    permission_classes = (IsOrgAdmin,)
    instance = None

    def perform_update(self, serializer):
        assets = serializer.validated_data.get('assets')
        instance = self.get_object()
        if instance != Node.root():
            instance.assets.remove(*tuple(assets))
        else:
            assets = [asset for asset in assets if asset.nodes.count() > 1]
            instance.assets.remove(*tuple(assets))


class NodeReplaceAssetsApi(generics.UpdateAPIView):
    serializer_class = serializers.NodeAssetsSerializer
    queryset = Node.objects.all()
    permission_classes = (IsOrgAdmin,)
    instance = None

    def perform_update(self, serializer):
        assets = serializer.validated_data.get('assets')
        instance = self.get_object()
        for asset in assets:
            asset.nodes.set([instance])


class RefreshNodeHardwareInfoApi(APIView):
    permission_classes = (IsOrgAdmin,)
    model = Node

    def get(self, request, *args, **kwargs):
        node_id = kwargs.get('pk')
        node = get_object_or_404(self.model, id=node_id)
        assets = node.get_all_assets()
        # task_name = _("更新节点资产硬件信息: {}".format(node.name))
        task_name = _("Update node asset hardware information: {}").format(node.name)
        task = update_assets_hardware_info_util.delay(assets, task_name=task_name)
        return Response({"task": task.id})


class TestNodeConnectiveApi(APIView):
    permission_classes = (IsOrgAdmin,)
    model = Node

    def get(self, request, *args, **kwargs):
        node_id = kwargs.get('pk')
        node = get_object_or_404(self.model, id=node_id)
        assets = node.get_all_assets()
        # task_name = _("测试节点下资产是否可连接: {}".format(node.name))
        task_name = _("Test if the assets under the node are connectable: {}".format(node.name))
        task = test_asset_connectivity_util.delay(assets, task_name=task_name)
        return Response({"task": task.id})


class RefreshAssetsAmount(APIView):
    permission_classes = (IsOrgAdmin,)
    model = Node

    def get(self, request, *args, **kwargs):
        self.model.expire_nodes_assets_amount()
        return Response("Ok")
