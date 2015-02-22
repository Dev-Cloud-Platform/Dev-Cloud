# -*- coding: utf-8 -*-
# @COPYRIGHT_begin
#
# Copyright [2015] Michał Szczygieł, M4GiK Software
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# @COPYRIGHT_end
from rest_framework import viewsets
from database.models.template_instances import TemplateInstances
from virtual_controller.api.serializers.template_instances_serializer import TemplateInstancesSerializer


class TemplateInstancesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows display list of all available templates.
    """
    queryset = TemplateInstances.objects.all()
    serializer_class = TemplateInstancesSerializer