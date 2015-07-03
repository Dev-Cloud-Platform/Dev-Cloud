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
from core.common.states import PUBLIC_IP_LIMIT, CM_ERROR, UNKNOWN_ERROR

from core.utils import celery
from core.utils.python_object_encoder import SetEncoder
from database.models.applications import Applications
from database.models.installed_applications import InstalledApplications
from database.models.template_instances import TemplateInstances
from database.models.virtual_machines import VirtualMachines
from virtual_controller.api.permissions import base_permissions as api_permissions
from virtual_controller.api.serializers.virtual_machines_serializer import VirtualMachinesSerializer
from virtual_controller.cc1_module.public_ip import NONE_AVAILABLE_PUBLIC_IP

from django.utils.translation import ugettext as _
from json import dumps
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


        A.D. Atomic
        Atomic blocks can be nested. In this case, when an inner block completes successfully, its effects can still be
        rolled back if an exception is raised in the outer block at a later point.

        @param request:
        @return:
        """

        virtual_machine_form = CreateVMForm

        virtual_machine_form.set_applications(
            request.DATA.get('applications', None) or request.query_params.get('applications', None))
        virtual_machine_form.set_template(
            request.DATA.get('template_id', None) or request.query_params.get('template_id', None))
        virtual_machine_form.set_workspace(
            request.DATA.get('workspace', None) or request.query_params.get('workspace', None))
        virtual_machine_form.set_public_ip(
            request.DATA.get('public_ip', None) or request.query_params.get('public_ip', None))
        virtual_machine_form.set_disk_space(
            request.DATA.get('disk_space', None) or request.query_params.get('disk_space', None))

        # Here do request to CC1.
        user_id = api_permissions.UsersPermission.get_user(request).id
        celery.create_virtual_machine.apply_async(args=(user_id, virtual_machine_form))

        virtual_machine = self.serializer_class.Meta.model.objects.create(
            disk_space=virtual_machine_form.get_disk_space(), public_ip=virtual_machine_form.get_public_ip(),
            template_instance_id=virtual_machine_form.get_template())

        for application in ast.literal_eval(virtual_machine_form.get_applications()):
            app = Applications.objects.get(application_name=application)
            InstalledApplications.objects.create(workspace=virtual_machine_form.get_workspace(),
                                                 user_id=user_id, application_id=app.id,
                                                 virtual_machine_id=virtual_machine.pk)

        return Response(status=status.HTTP_200_OK)