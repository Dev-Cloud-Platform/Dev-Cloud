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
import jsonpickle
from rest_framework import viewsets, status
from rest_framework.decorators import list_route
from rest_framework.response import Response

from core.common.states import PUBLIC_IP_LIMIT, CM_ERROR, UNKNOWN_ERROR, FAILED
from core.utils import celery
from core.utils.log import error
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
    def create_virtual_machine(self, request):
        """
        Creates virtual machine.
        @param request:
        @return: Status about creation of virtual machine.
                 If everything is OK return code 200 with VirtualMachinesSerializer serializer class,
                 if not return code 400 for bad request, or 417 if creation of virtual machine goes wrong.
        """
        user_id = api_permissions.UsersPermission.get_user(request).id
        vm_id = None
        virtual_machine_form = CreateVMForm()

        if virtual_machine_form.is_valid(request):
            try:
                # Here do request to CC1.
                pickle_vm = jsonpickle.encode(virtual_machine_form)
                vm_id = celery.create_virtual_machine.apply_async(args=(user_id, pickle_vm)).get()
                if vm_id != FAILED:
                    virtual_machine = self.serializer_class.Meta.model.objects.get(vm_id=vm_id)
                    serializer = self.get_serializer(virtual_machine)
                    celery.init_virtual_machine.apply_async(
                        args=(user_id, serializer.data, virtual_machine_form.get_applications()))

                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(status=status.HTTP_417_EXPECTATION_FAILED)
            except Exception as ex:
                error(user_id, str(ex))
                # Destroy created virtual machine:
                if vm_id is not None:
                    celery.destroy_virtual_machine.apply_async(
                        args=(api_permissions.UsersPermission.get_user(request).id, vm_id))
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['get'], url_path='get-vm-status')
    def get_virtual_machine_status(self, request):
        """
        Returns requested caller's VM.
        @param request:
        @return: number status of virtual machine:
                'init': 0,
                'running': 1,
                'closing': 2,
                'closed': 3,
                'saving': 4,
                'failed': 5,
                'saving failed': 6,
                'running ctx': 7,
                'restart': 8,
                'suspend': 9,
                'turned off': 10,
                'erased': 11,
                'erasing': 12
        """
        vm_id = request.DATA.get('vm_id', None) or request.query_params.get('vm_id', None)
        if vm_id:
            user_id = api_permissions.UsersPermission.get_user(request).id
            return Response(celery.get_virtual_machine_status.apply_async(args=(user_id, vm_id)).get())
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['get'], url_path='generate-ssh-key')
    def generate_ssh_key(self, request):
        """
        Generates ssh key pair. Public part of that Key is
        stored in CC1 database with specified name, whereas content of the private Key
        part is returned and stored in DevCloud database.
        Neither public, nor private part of the key is saved to file.
        @param request:
        @return: Private part of the key.
        """
        key_name = request.DATA.get('key_name', None) or request.query_params.get('key_name', None)
        if key_name:
            user_id = api_permissions.UsersPermission.get_user(request).id
            return Response(celery.generate_ssh_key.apply_async(args=(user_id, key_name)).get())
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['get'], url_path='get-ssh-key')
    def get_ssh_key(self, request):
        """
        Get ssh key. The public part.
        @param request:
        @return: Public part of the key.
        """
        key_name = request.DATA.get('key_name', None) or request.query_params.get('key_name', None)
        if key_name:
            user_id = api_permissions.UsersPermission.get_user(request).id
            return Response(celery.get_ssh_key.apply_async(args=(user_id, key_name)).get())
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['post', 'get'], url_path='destroy-vm')
    def destroy_virtual_machine(self, request):
        """
        Destroys given virtual machine.
        @param request:
        @return: Status OK if everything goes fine, another way failed status.
        """
        vm_id = request.DATA.get('vm_id', None) or request.query_params.get('vm_id', None)
        if vm_id:
            user_id = api_permissions.UsersPermission.get_user(request).id
            return Response(celery.destroy_virtual_machine.apply_async(args=(user_id, vm_id)).get())
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['get'], url_path='get-vnc-data')
    def get_vnc_data(self, request):
        """
        Returns data for VNC connection.
        @param request:
        @return: Dict of data contains host, port and password.
        """
        vm_id = request.DATA.get('vm_id', None) or request.query_params.get('vm_id', None)
        if vm_id:
            user_id = api_permissions.UsersPermission.get_user(request).id
            return Response(celery.get_vnc.apply_async(args=(user_id, vm_id)).get())
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
