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
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, status
from rest_framework.decorators import list_route
from rest_framework.response import Response
from database.models.template_instances import TemplateInstances
from virtual_controller.api.serializers.template_instances_serializer import TemplateInstancesSerializer


class TemplateInstancesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows display list of all available templates.
    """
    queryset = TemplateInstances.objects.all()
    serializer_class = TemplateInstancesSerializer

    @list_route(methods=['get'], url_path='get-template')
    def get_template(self, request):
        """
        Gets available templates for VM.
        You need add payload with key as template_id and your id of template as value.
        Example: GET /rest_api/template-instances/get-template/?template_id=1
        @param request:
        @return:
        """
        template_id = request.DATA.get('template_id', None) or request.query_params.get('template_id', None)
        if template_id:
            try:
                template = TemplateInstances.objects.get(template_id=template_id)
                serializer = self.get_serializer(template)
                return Response(serializer.data)
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)