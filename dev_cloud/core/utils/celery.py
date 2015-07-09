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
from celery import Celery

from core.settings.common import settings
from core.settings.common import BROKER_URL, CELERY_RESULT_BACKEND
from virtual_controller.cc1_module.check_quota import Quota
from virtual_controller.cc1_module.public_ip import PoolIP


# os.environ.setdefault('CELERY_CONFIG_MODULE', "core.settings.%s" % args)
from virtual_controller.cc1_module.virtual_machine import VirtualMachine

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
def request(user_id):
    """
    Method to obtain public IP form CC1.
    @return: Obtained IP.
    """
    poolIP = PoolIP(user_id)
    poolIP.request()

    return poolIP.get_ip_address()


@app.task(trail=True, name='core.utils.tasks.release')
def release(user_id, ip_address):
    """
    Method to release public IP form CC1.
    @return: Status about removed ip address.
    """
    poolIP = PoolIP(user_id, ip_address)
    return poolIP.remove()


@app.task(trail=True, name='core.utils.tasks.check_resource')
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
def create_virtual_machine(user_id, vm_property):
    """
    Creates new instance of virtual machine on CC1, making a request.
    @param user_id: id of caller.
    @param vm_property: instance of virtual machine form with properties.
    @return:
    """
    virtual_machine = VirtualMachine(user_id, vm_property)
    return virtual_machine.create()