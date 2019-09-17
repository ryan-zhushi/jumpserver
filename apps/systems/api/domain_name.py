# -*- coding: utf-8 -*-

from rest_framework_bulk import BulkModelViewSet
from rest_framework.pagination import LimitOffsetPagination

from common.permissions import IsOrgAdmin
from common.mixins import IDInCacheFilterMixin
from common.utils import get_logger
from ..models import DomainName
from ..serializers import DomainNameSerializer

logger = get_logger(__name__)
__all__ = [
    'DomainNameViewSet',
]


class DomainNameViewSet(IDInCacheFilterMixin, BulkModelViewSet):
    filter_fields = ('name', 'ip', 'type', 'comment')
    search_fields = filter_fields
    queryset = DomainName.objects.all()
    serializer_class = DomainNameSerializer
    permission_class = IsOrgAdmin
    pagination_class = LimitOffsetPagination

