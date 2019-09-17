# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from common.mixins import BulkSerializerMixin
from common.serializers import AdaptedBulkListSerializer
from ..models import DomainName


class DomainNameSerializer(BulkSerializerMixin, serializers.ModelSerializer):

    class Meta:
        model = DomainName
        list_serializer_class = AdaptedBulkListSerializer
        fields = [
            'id', 'name', 'ip', 'type', 'comment', 'is_active',
        ]

