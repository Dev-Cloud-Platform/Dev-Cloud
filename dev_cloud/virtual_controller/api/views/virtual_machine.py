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
import ast
import json
from django.db.transaction import atomic
from rest_framework import viewsets, status
from rest_framework.decorators import list_route
from rest_framework.response import Response
from core.common.states import PUBLIC_IP_LIMIT, CM_ERROR, UNKNOWN_ERROR, FAILED

from core.utils import celery
from core.utils.python_object_encoder import SetEncoder
from database.models.applications import Applications
from database.models.installed_applications import InstalledApplications
from database.models.virtual_machines import VirtualMachines
from virtual_controller.api.permissions import base_permissions as api_permissions
from virtual_controller.api.serializers.virtual_machines_serializer import VirtualMachinesSerializer
from virtual_controller.cc1_module.public_ip import NONE_AVAILABLE_PUBLIC_IP
from web_service.forms.enviroment.create_vm import CreateVMForm


class VirtualMachineList(viewsets.ReadOnlyModelViewSet):
    """
    List of all available virtual machines.
    """
    queryset = VirtualMachines.objects.all()
    serializer_class = VirtualMachinesSerializer
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
        if result == PUBLIC_IP_LIMIT:
            result = NONE_AVAILABLE_PUBLIC_IP
        elif result == CM_ERROR:
            result = CM_ERROR
        elif result == "":
            result = UNKNOWN_ERROR

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
        You need add payload with key as template_id and your id of template as value.
        Example: GET /rest_api/virtual-machines/resource-test/?template_id=1
        @param request:
        @return: Status about available resources. If is ok return 200, if not return 402.
        """
        template_id = request.DATA.get('template_id', None) or request.query_params.get('template_id', None)
        if template_id:
            user_id = api_permissions.UsersPermission.get_user(request).id
            return Response(status=celery.check_resource.apply_async(args=(user_id, template_id)).get())
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['post', 'get'], url_path='create-vm')
    @atomic
    def create_virtual_machine(self, request):
        """
        Creates virtual machine.

        A.D. Atomic
        Atomic blocks can be nested. In this case, when an inner block completes successfully, its effects can still be
        rolled back if an exception is raised in the outer block at a later point.

        @param request:
        @return: Status about creation of virtual machine.
                 If everything is OK return code 200 with VirtualMachinesSerializer serializer class,
                 if not return code 400 for bad request, or 417 if creation of virtual machine goes wrong.
        """

        virtual_machine_form = CreateVMForm()

        if virtual_machine_form.is_valid(request):
            # Here do request to CC1.
            user_id = api_permissions.UsersPermission.get_user(request).id
            vm_id = celery.create_virtual_machine.apply_async(args=(user_id, virtual_machine_form)).get()
            if vm_id != FAILED:
                virtual_machine = self.serializer_class.Meta.model.objects.create(
                    vm_id=vm_id, disk_space=virtual_machine_form.get_disk_space(),
                    public_ip=virtual_machine_form.get_public_ip(),
                    template_instance_id=virtual_machine_form.get_template())
                serializer = self.get_serializer(virtual_machine)

                for application in ast.literal_eval(virtual_machine_form.get_applications()):
                    app = Applications.objects.get(application_name=application)
                    InstalledApplications.objects.create(workspace=virtual_machine_form.get_workspace(),
                                                         user_id=user_id, application_id=app.id,
                                                         virtual_machine_id=virtual_machine.pk)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_417_EXPECTATION_FAILED)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['get'], url_path='get-vm-status')
    def get_virtual_machine(self, request):
        """
        Returns requested caller's VM.
        @param request:
        @return:
        """
        vm_id = request.DATA.get('vm_id', None) or request.query_params.get('vm_id', None)
        if vm_id:
            user_id = api_permissions.UsersPermission.get_user(request).id
            return Response(celery.get_virtual_machine_status.apply_async(args=(user_id, vm_id)).get())
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)