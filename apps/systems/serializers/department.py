# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from common.mixins import BulkSerializerMixin
from common.serializers import AdaptedBulkListSerializer
from ..models import Department


class DepartmentSerializer(BulkSerializerMixin, serializers.ModelSerializer):

    class Meta:
        model = Department
        list_serializer_class = AdaptedBulkListSerializer
        fields = [
            'id', 'name', 'principal', 'principal_duty', 'principal_ecard', 'principal_email', 'principal_phone', 'coordinator', 'coordinator_duty', 'coordinator_ecard', 'coordinator_email', 'coordinator_phone', 'coordinator_qq'
        ]

