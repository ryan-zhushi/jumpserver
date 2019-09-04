# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from common.mixins import BulkSerializerMixin
from common.serializers import AdaptedBulkListSerializer
from ..models import System


class SystemSerializer(BulkSerializerMixin, serializers.ModelSerializer):

    class Meta:
        model = System
        list_serializer_class = AdaptedBulkListSerializer
        fields = [
            'id', 'name', 'homepage_url', 'admin_url', 'admin_staff',
            'admin_staff_phone', 'department',
        ]