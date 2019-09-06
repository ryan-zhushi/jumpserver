#!/usr/bin/env python
# ~*~ coding: utf-8 ~*~
#
from __future__ import absolute_import

from rest_framework_bulk.routes import BulkRouter

from .. import api

app_name = 'systems'

router = BulkRouter()
router.register(r'systems', api.SystemViewSet, 'system')
router.register(r'departments', api.DepartmentViewSet, 'department')

urlpatterns = [

]

urlpatterns += router.urls
