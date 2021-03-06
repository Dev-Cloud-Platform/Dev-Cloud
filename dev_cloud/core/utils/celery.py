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
import jsonpickle
from django.utils.translation import ugettext as _

from core.common import states
from core.common.states import FAILED, OK, NOT_ALLOWED
from core.settings.common import settings, WAIT_TIME, LOOP_TIME
from core.settings.common import BROKER_URL, CELERY_RESULT_BACKEND
from core.settings.config import SSH_KEY_PATH
from core.utils.auth import ROOT
from core.utils.decorators import dev_cloud_task
from core.utils.log import error
from database.models import Applications, InstalledApplications, VirtualMachines
from database.models.vm_tasks import TASK_ID, VmTasks
from virtual_controller.cc1_module.check_quota import Quota
from virtual_controller.cc1_module.key import Key
from virtual_controller.cc1_module.public_ip import PoolIP



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
INITIALIZE_VNC = _('Initialize VNC connection')

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
def request(user_id, *args):
    """
    Method to obtain public IP form CC1.
    @return: Obtained IP.
    """
    poolIP = PoolIP(user_id)
    poolIP.request()
    return poolIP.get_ip_address()


@app.task(trail=True, name='core.utils.tasks.release')
@dev_cloud_task(RELEASE_IP)
def release(user_id, ip_address, *args):
    """
    Method to release public IP form CC1.
    @return: Status about removed ip address.
    """
    poolIP = PoolIP(user_id, ip_address)
    return poolIP.remove()


@app.task(trail=True, name='core.utils.tasks.check_resource')
@dev_cloud_task(CHECK_RESOURCE)
def check_resource(user_id, template_id, *args):
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
def create_virtual_machine(user_id, vm_property, *args):
    """
    Creates new instance of virtual machine on CC1, making a request.
    @param user_id: id of caller.
    @param vm_property: instance of virtual machine form with properties.
    @return: id of virtual machine.
    """
    virtual_machine_form = jsonpickle.decode(vm_property)
    virtual_machine = VirtualMachine(user_id, virtual_machine_form)
    vm_id = virtual_machine.create()

    if vm_id:
        try:
            if virtual_machine_form.get_public_ip() != 'False':
                public_ip = virtual_machine.get_vm_public_ip(vm_id)
            else:
                public_ip = virtual_machine_form.get_public_ip()

            virtual_machine = VirtualMachines.objects.create(
                vm_id=vm_id, disk_space=virtual_machine_form.get_disk_space(),
                public_ip=public_ip,
                private_ip=virtual_machine.get_vm_private_ip(vm_id),
                ssh_key=virtual_machine_form.get_ssh_private_key(),
                template_instance_id=virtual_machine_form.get_template())

            for application in ast.literal_eval(virtual_machine_form.get_applications()):
                app = Applications.objects.get(application_name=application)
                InstalledApplications.objects.create(workspace=virtual_machine_form.get_workspace(),
                                                     user_id=user_id, application_id=app.id,
                                                     virtual_machine_id=virtual_machine.pk)

            VmTasks.objects.create(vm_id=virtual_machine.id, task_id=args[0].get(TASK_ID))
        except Exception, ex:
            error(args[0], _("DataBase - Problem with create virtual machine") + str(ex))

    return vm_id


# @app.task(trail=True, name='core.utils.tasks.get_virtual_machine_status')
def get_virtual_machine_status(user_id, vm_id, *args):
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
def generate_ssh_key(user_id, name, *args):
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
def init_virtual_machine(user_id, vm_serializer_data, applications, *args):
    """
    Initialize given virtual machine with selected application stored in database.
    @param user_id: id of caller.
    @param vm_serializer_data: serialized data contains information about virtual machines.
    @param applications: list of applications.
    @return:
    """
    vm_model = VirtualMachines.objects.get(vm_id=vm_serializer_data.get('vm_id'))
    try:
        VmTasks.objects.create(
            vm_id=vm_model.id,
            task_id=args[0].get(TASK_ID))
    except Exception, ex:
        error(args[0], _("Database - Problem with initialize virtual machine") + str(ex))

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
        # ssh = RunRemoteCommand(virtual_machine.get_vm_private_ip(vm_serializer_data.get('vm_id')),
        #                        ROOT, SSH_KEY_PATH, VM_IMAGE_ROOT_PASSWORD)
        ssh = SSHConnector(virtual_machine.get_vm_private_ip(vm_serializer_data.get('vm_id')), ROOT,
                           SSH_KEY_PATH)
        # ssh_key = StringIO.StringIO()
        # ssh_key.write(vm_model.ssh_key.replace('\\n', '\n').replace('"', ''))
        # ssh = SSHConnector(vm_model.public_ip, ROOT, '/home/m4gik/.ssh/DevCloud')

        ssh.exec_task(init_juju_on_vm)

        for application in ast.literal_eval(applications):
            app = Applications.objects.get(application_name=application)
            ssh.call_remote_command(app.instalation_procedure)
            ssh.check_juju_status(application, user_id)

        ssh.close_connection()
    else:
        raise Exception


# @app.task(trail=False, ignore_result=True, name='core.utils.tasks.destroy_virtual_machine')
@dev_cloud_task(DESTROY_VM)
def destroy_virtual_machine(user_id, vm_id, *args):
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

    try:
        own_machine = VirtualMachines.objects.get(vm_id=vm_id)
        installed_apps = InstalledApplications.objects.filter(user__id=int(user_id),
                                                              virtual_machine__id=int(own_machine.id))
    except:
        installed_apps = None
        own_machine = None

    if virtual_machine.check_vm_property(user_id, vm_id):
        virtual_machine = VirtualMachine(user_id)
        destroy_status = virtual_machine.destroy(vm_id)
        if destroy_status == OK:
            if own_machine.public_ip != "False":
                while virtual_machine.get_vm_status(vm_id) != \
                        [key for key, value in states.vm_states.iteritems() if value == 'closed'][0]:
                    current_time += 1
                    is_timeout = SSHConnector.timeout(WAIT_TIME, 1, current_time)
                    if is_timeout:
                        break
                release(user_id, own_machine.public_ip)
            own_machine.delete()
            installed_apps.delete()
            return OK
        else:
            return FAILED
    else:
        return FAILED


@app.task(trail=True, name='core.utils.tasks.get_vnc')
@dev_cloud_task(INITIALIZE_VNC)
def get_vnc(user_id, vm_id, *args):
    """
    Gets VNC data to connect.
    @param user_id: id of caller.
    @param vm_id: id of virtual machine.
    @return: Dict of data contains host, port and password.
    """
    try:
        VmTasks.objects.create(
            vm_id=VirtualMachines.objects.get(vm_id=vm_id).id,
            task_id=args[0].get(TASK_ID))
    except Exception, ex:
        error(args[0], _("Database - Problem with initialize VNC") + str(ex))

    virtual_machine = VirtualMachine(user_id)

    if virtual_machine.check_vm_property(user_id, vm_id):
        return virtual_machine.get_no_vnc_data(vm_id)
    else:
        return NOT_ALLOWED


# @app.task(trail=True, name='core.utils.tasks.get_cpu_load')
def get_cpu_load(user_id, vm_id, *args):
    """
    Gets CPU load data.
    @param user_id: id of caller.
    @param vm_id: id of virtual machine.
    @return: Dict of data contains CPU load for 1, 5, 15 minutes.
    """
    virtual_machine = VirtualMachine(user_id)

    if virtual_machine.check_vm_property(user_id, vm_id):
        return virtual_machine.get_cpu_load(vm_id)
    else:
        return NOT_ALLOWED
