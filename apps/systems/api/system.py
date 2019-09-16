# -*- coding: utf-8 -*-

from rest_framework_bulk import BulkModelViewSet
from rest_framework.pagination import LimitOffsetPagination

from common.permissions import IsValidUser
from common.mixins import IDInCacheFilterMixin
from common.utils import get_logger
from ..models import System
from ..serializers import SystemSerializer

logger = get_logger(__name__)
__all__ = [
    'SystemViewSet', 
]


class SystemViewSet(IDInCacheFilterMixin, BulkModelViewSet):
    filter_fields = ('id', 'name', 'homepage_url', 'department')
    search_fields = filter_fields
    queryset = System.objects.all()
    serializer_class = SystemSerializer
    permission_classes = (IsValidUser,)
    pagination_class = LimitOffsetPagination
    
    def get_queryset(self):
        if not self.request.user.is_superuser:
            self.queryset = self.request.user.department.systems
        return self.queryset
