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
import copy
import json
import requests
from core.common.states import OK, STATUS, FAILED, DATA
from core.settings.config import VM_IMAGE_NAME
from core.utils import log
from virtual_controller.cc1_module import address_clm, payload as payload_org
from virtual_controller.cc1_module.logger import error
from virtual_controller.cc1_module.master_user import MasterUser
from virtual_controller.cc1_module.public_ip import PoolIP
from django.utils.translation import ugettext as _


class VirtualMachine(object):
    """
    Class responsible for demonize request to managing virtual machines.
    """

    vm_property = None
    user_id = None
    caller_id = None
    name = None
    description = None
    image_id = None
    template_id = None
    public_ip_id = None
    iso_list = None
    disk_list = None
    vnc = None
    groups = None
    count = 1
    user_data = None
    ssh_key = None
    ssh_username = None

    def __init__(self, user_id, vm_property=None):
        """
        Constructor for VirtualMachine which assign basic properties.
        @param user_id: Id of caller
        @param vm_property: Optional argument, which assign properties for instance.
        """
        self.user_id = user_id
        self.vm_property = vm_property

    def init(self):
        """
        Initializes based value for request to create virtual machine.
        @return: Object of poolIP.
        """
        self.caller_id = MasterUser.get_info_data().get('user_id')
        self.name = 'DevCloud_' + str(self.user_id) + '_' + self.vm_property.get_workspace()
        self.description = 'Virtual machine created by Dev Cloud, named: ' + self.name

        for image in MasterUser.get_images_list():
            if image.get('name') == VM_IMAGE_NAME:
                self.image_id = image.get('system_image_id')

        poolIP = None
        if self.vm_property.get_public_ip() == 'True':
            poolIP = PoolIP(self.user_id)
            if poolIP.request() == OK:
                self.public_ip_id = poolIP.get_public_ip_id()

        self.template_id = self.vm_property.get_template()
        self.iso_list = None
        self.disk_list = None
        # self.groups = MasterUser.get_groups()
        return poolIP

    def get_vm_property(self):
        return self.vm_property

    def set_vm_property(self, vm_property):
        self.vm_property = vm_property

    def create(self):
        """
        Creates virtual machines.
        @return: id of virtual machine if everything goes fine, another way failed status.
        """
        poolIP = self.init()

        payload = copy.deepcopy(payload_org)
        payload['caller_id'] = self.caller_id
        payload['name'] = self.name
        payload['description'] = self.description
        payload['image_id'] = self.image_id
        payload['template_id'] = self.template_id
        payload['public_ip_id'] = self.public_ip_id
        payload['iso_list'] = self.iso_list
        payload['disk_list'] = self.disk_list
        payload['vnc'] = self.vnc
        # payload['groups'] = self.groups
        payload['count'] = self.count
        payload['user_data'] = self.user_data
        payload['ssh_key'] = self.ssh_key
        payload['ssh_username'] = self.ssh_username

        vm = requests.post(address_clm + 'user/vm/create/', data=json.dumps(payload))

        if vm.status_code == 200 and ast.literal_eval(vm.text).get(STATUS) == OK:
            return ast.literal_eval(vm.text).get(DATA)[0].get('vm_id')
        else:
            error(None, vm)
            if payload.get('public_ip_id') is not None:
                poolIP.remove()
            return FAILED

    @classmethod
    def destroy(cls, vm_ids):
        """
        This function only destroys VM.

        All the cleanup (removing disk, saving, rescuing resources, ...) is done by hook through
        contextualization.update_vm method (yeah, intuitive).

        Simple sequence diagram:
        DevCloud        CLM        CM         CTX           Node (HOOK)
            .            .
         destroy ---->Destroy -->destroy
                         |          |       (LV.destroy)
                         |          |------------------------->HookScript
                         .          .                          |
                         .          .          ctx.update_vm<--|
                         .          .           |              |
                         .          .           |------------->cp
                         .          .           |------------->rm
                         .          .          update_resources

        @param vm_ids: list of virtual machines' ids.
        @return:  Status OK if everything goes fine, another way failed status.
        """
        payload = copy.deepcopy(payload_org)
        payload['vm_ids'] = vm_ids
        vm = requests.post(address_clm + 'user/vm/destroy/', data=json.dumps(payload))

        if vm.status_code == 200 and ast.literal_eval(vm.text).get(STATUS) == OK:
            return OK
        else:
            error(None, vm)
            return FAILED

    def detach_vnc(self):
        pass

    def edit(self):
        pass

    def get_by_id(self):
        pass

    def get_list(self):
        pass

    def reset(self):
        pass

    def save_and_shutdown(self):
        pass

    @classmethod
    def get_vm_status(cls, vm_id):
        """
        Returns requested caller's VM.
        @param vm_id: id of virtual machine.
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
        payload = copy.deepcopy(payload_org)
        payload['vm_id'] = vm_id

        vm = requests.post(address_clm + 'user/vm/get_by_id/', data=json.dumps(payload))
        if vm.status_code == 200 and json.loads(vm.text).get(STATUS) == OK:
            return json.loads(vm.text).get(DATA).get('state')
        else:
            log.error(None, _("CC1 - Problem with request: ") + vm.url)
            return FAILED