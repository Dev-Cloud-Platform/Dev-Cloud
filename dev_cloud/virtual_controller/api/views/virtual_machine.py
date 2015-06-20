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
from rest_framework import viewsets, status
from rest_framework.decorators import list_route
from rest_framework.response import Response

from core.utils import celery
from core.utils.python_object_encoder import SetEncoder
from database.models.virtual_machines import VirtualMachines
from virtual_controller.api.serializers.installed_applications_serializer import InstalledApplicationsSerializer
from virtual_controller.api.permissions import base_permissions as api_permissions
from virtual_controller.cc1_module.public_ip import NONE_AVAILABLE_PUBLIC_IP

from django.utils.translation import ugettext as _
from json import dumps


class VirtualMachineList(viewsets.ReadOnlyModelViewSet):
    """
    List of all available virtual machines.
    """
    queryset = VirtualMachines.objects.all()
    serializer_class = InstalledApplicationsSerializer
    permission_classes = {api_permissions.UsersPermission}

    @list_route(methods=['get'], url_path='obtain-ip')
    def obtain_ip(self, request):
        """
        Gets available IP address.
        @param request:
        @return: Public IP address.
        """
        user_id = api_permissions.UsersPermission.get_user(request).id
        result = celery.request.apply_async(args=(user_id,)).get()
        # j = dumps(result, cls=SetEncoder)
        if result == "":
            result = NONE_AVAILABLE_PUBLIC_IP

        return Response(result)

    @list_route(methods=['get'], url_path='release-ip')
    def release_ip(self, request):
        """
        Release give ip address.
        You need add payload with key as ip and your ip address as value.
        Example: GET /rest_api/virtual-machines/release-ip/?ip=192.168.1.1
        @param request:
        @return: status code.
        """
        ip_to_release = request.DATA.get('ip', None) or request.query_params.get('ip', None)
        if ip_to_release:
            user_id = api_permissions.UsersPermission.get_user(request).id
            celery.release.apply_async(args=(user_id, ip_to_release))
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


    @list_route(methods=['get'], url_path='resource-test')
    def resource_test(self, request):
        """
        Test possibility of future allocated resources for VM.
        Based on quota.
        You need add payload with key as template_id and your if of template as value.
        Example: GET /rest_api/virtual-machines/resource-test/?template_id=1
        @param request:
        @return:
        """
        template_id = request.DATA.get('template_id', None) or request.query_params.get('template_id', None)
        if template_id:
            user_id = api_permissions.UsersPermission.get_user(request).id
            return Response(status=celery.check_resource.apply_async(args=(user_id, template_id)))
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)