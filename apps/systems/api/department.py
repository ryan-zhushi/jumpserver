# -*- coding: utf-8 -*-

from rest_framework_bulk import BulkModelViewSet
from rest_framework.pagination import LimitOffsetPagination

from common.permissions import IsOrgAdmin
from common.mixins import IDInCacheFilterMixin
from common.utils import get_logger
from ..models import Department
from ..serializers import DepartmentSerializer

logger = get_logger(__name__)
__all__ = [
    'DepartmentViewSet',
]


class DepartmentViewSet(IDInCacheFilterMixin, BulkModelViewSet):
    filter_fields = ('name', 'principal', 'principal_duty', 'principal_ecard', 'principal_email', 'principal_phone', 'coordinator', 'coordinator_duty', 'coordinator_ecard', 'coordinator_email', 'coordinator_phone', 'coordinator_qq')
    search_fields = filter_fields
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_class = IsOrgAdmin
    pagination_class = LimitOffsetPagination

