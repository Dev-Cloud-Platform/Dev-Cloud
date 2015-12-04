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
from __future__ import absolute_import
import ast
from celery import Celery
from fabric.decorators import hosts
from fabric.operations import run
from fabric.tasks import execute
import jsonpickle
import paramiko
from core.common import states

from core.settings.common import settings, WAIT_TIME, LOOP_TIME
from core.settings.common import BROKER_URL, CELERY_RESULT_BACKEND
from core.settings.config import SSH_KEY_PATH, VM_IMAGE_ROOT_PASSWORD
from core.utils.auth import ROOT
from core.utils.decorators import dev_cloud_task
from core.utils.exception import DevCloudException
from database.models import Applications
from virtual_controller.cc1_module.check_quota import Quota
from virtual_controller.cc1_module.key import Key
from virtual_controller.cc1_module.public_ip import PoolIP
from django.utils.translation import ugettext as _


# os.environ.setdefault('CELERY_CONFIG_MODULE', "core.settings.%s" % args)
from virtual_controller.cc1_module.virtual_machine import VirtualMachine
from virtual_controller.juju_core.juju_installation_procedure import init_juju_on_vm
from virtual_controller.juju_core.ssh_connector import SSHConnector

REQUEST_IP = _('Request new IP')
RELEASE_IP = _('Release IP')
CHECK_RESOURCE = _('Check resource')
CREATE_VM = _('Create new virtual machine')
GENERATE_SSH = _('Generate new SSH key pair')
INIT_VM = _('Initialize virtual machine')
DESTROY_VM = _('Destroy virtual machine')

app = Celery('core.utils', broker=BROKER_URL, backend=CELERY_RESULT_BACKEND, include=['core.utils'])

# Optional configuration, see the application user guide.
app.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
)

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object("django.conf:settings")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


# if __name__ == '__main__':
# app.start()


@app.task(trail=True, name='core.utils.tasks.request')
@dev_cloud_task(REQUEST_IP)
def request(user_id):
    """
    Method to obtain public IP form CC1.
    @return: Obtained IP.
    """
    poolIP = PoolIP(user_id)
    poolIP.request()
    return poolIP.get_ip_address()


@app.task(trail=True, name='core.utils.tasks.release')
@dev_cloud_task(RELEASE_IP)
def release(user_id, ip_address):
    """
    Method to release public IP form CC1.
    @return: Status about removed ip address.
    """
    poolIP = PoolIP(user_id, ip_address)
    return poolIP.remove()


@app.task(trail=True, name='core.utils.tasks.check_resource')
@dev_cloud_task(CHECK_RESOURCE)
def check_resource(user_id, template_id):
    """
    Method to check available resource to create new virtual machine.
    @param user_id: id of caller.
    @param template_id: selected id for template.
    @return: Status about available resources. If is ok return 200, if not return 402.
    """
    quota = Quota(user_id)
    quota.check_quota(template_id)

    return quota.get_status()


@app.task(trail=True, name='core.utils.tasks.create_virtual_machine')
@dev_cloud_task(CREATE_VM)
def create_virtual_machine(user_id, vm_property):
    """
    Creates new instance of virtual machine on CC1, making a request.
    @param user_id: id of caller.
    @param vm_property: instance of virtual machine form with properties.
    @return: id of virtual machine.
    """
    virtual_machine = VirtualMachine(user_id, jsonpickle.decode(vm_property))
    return virtual_machine.create()


@app.task(trail=True, name='core.utils.tasks.get_virtual_machine_status')
def get_virtual_machine_status(user_id, vm_id):
    """
    Gets requested caller's virtual machine.
    @param user_id: id of caller.
    @param vm_id: id of virtual machine.
    @return: data contains information about virtual machine.
    """
    virtual_machine = VirtualMachine(user_id)
    return virtual_machine.get_vm_status(vm_id)


@app.task(trail=True, name='core.utils.tasks.generate_ssh_key')
@dev_cloud_task(GENERATE_SSH)
def generate_ssh_key(user_id, name):
    """
    Generates ssh key pair. Public part of that Key is
    stored in CC1 database with specified name, whereas content of the private Key
    part is returned and stored in DevCloud database.
    Neither public, nor private part of the key is saved to file.
    @param user_id: id of caller.
    @param name: Key's name.
    @return: Private part of the key.
    """
    key = Key(user_id, name)
    return key.generate()


@app.task(trail=True, name='core.utils.tasks.get_ssh_key')
def get_ssh_key(user_id, name):
    """
    Get ssh key. The public part.
    @param user_id: id of caller.
    @param name: Key's name.
    @return: Public part of the key.
    """
    key = Key(user_id, name)
    return key.get(name)


@app.task(trail=False, ignore_result=True, name='core.utils.tasks.init_virtual_machine')
@dev_cloud_task(INIT_VM)
def init_virtual_machine(user_id, vm_serializer_data, applications):
    """
    Initialize given virtual machine with selected application stored in database.
    @param user_id: id of caller.
    @param vm_serializer_data: serialized data contains information about virtual machines.
    @param applications: list of applications.
    @return:
    """
    try:
        is_timeout = False
        current_time = 0
        virtual_machine = VirtualMachine(user_id)
        while virtual_machine.get_vm_status(vm_serializer_data.get('vm_id')) != \
                [key for key, value in states.vm_states.iteritems() if value == 'running ctx'][0]:
            current_time += LOOP_TIME
            is_timeout = SSHConnector.timeout(WAIT_TIME, LOOP_TIME, current_time)
            if is_timeout:
                break

        if not is_timeout:
            ssh = SSHConnector(virtual_machine.get_vm_private_ip(vm_serializer_data.get('vm_id')), ROOT,
                               SSH_KEY_PATH)

            ssh.exec_task(init_juju_on_vm)

            for application in ast.literal_eval(applications):
                app = Applications.objects.get(application_name=application)
                ssh.call_remote_command(app.instalation_procedure)
    except Exception:
        raise DevCloudException('init_vm')


@app.task(trail=False, ignore_result=True, name='core.utils.tasks.destroy_virtual_machine')
@dev_cloud_task(DESTROY_VM)
def destroy_virtual_machine(user_id, vm_id):
    """
    Destroys the given virtual machine.
    @param user_id: id of caller.
    @param vm_id: id of virtual machine.
    @return: OK if machine is properly destroyed or FAILED if not.
    """
    current_time = 0
    virtual_machine = VirtualMachine(user_id)
    while virtual_machine.get_vm_status(vm_id) != \
            [key for key, value in states.vm_states.iteritems() if value == 'running ctx'][0]:
        current_time += LOOP_TIME
        is_timeout = SSHConnector.timeout(WAIT_TIME, LOOP_TIME, current_time)
        if is_timeout:
            break

    virtual_machine = VirtualMachine(user_id)
    return virtual_machine.destroy(vm_id)
