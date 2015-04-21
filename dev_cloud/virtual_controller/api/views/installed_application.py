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
from core.utils.python_object_encoder import SetEncoder
from database.models.installed_applications import InstalledApplications
from virtual_controller.api.serializers.installed_applications_serializer import InstalledApplicationsSerializer
from virtual_controller.api.permissions import base_permissions as api_permissions
from rest_framework.decorators import list_route
from rest_framework.response import Response
from virtual_controller.cc1_module.public_ip import request as new_ip_request, get_list, release
from virtual_controller.tasks import reserved_pool_ip
from json import dumps


class InstalledApplicationList(viewsets.ReadOnlyModelViewSet):
    """
    List of all available applications.
    """
    queryset = InstalledApplications.objects.all()
    serializer_class = InstalledApplicationsSerializer
    permission_classes = {api_permissions.UsersPermission}

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @list_route(methods=['get'], url_path='obtain-ip')
    def obtain_ip(self, request):
        """
        Gets available IP address.
        @param request:
        @return: Public IP address.
        """
        # TODO : Implement method to obtain public IP form CC1.
        result = reserved_pool_ip.add(2, 11)
        # result = reserved_pool_ip.sleeptask.delay(10)
        # result_two = reserved_pool_ip.sleeptask.delay(10)
        j = dumps(result, cls=SetEncoder)
        # release(28)
        return Response(j)