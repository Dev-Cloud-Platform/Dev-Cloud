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
import json
import time
import sys

from fabric.api import execute, run, env
from fabric.network import disconnect_all
from core.settings.common import LOOP_TIME, WAIT_TIME
from core.settings.config import VM_IMAGE_ROOT_PASSWORD
from core.utils.log import error
from virtual_controller.juju_core.juju_instance import JujuInstance


class SSHConnector(object):
    """
    Class responsible for provide secure connection between dev cloud app and client virtual machine.
    """

    def __init__(self, host, user, key):
        env.host_string = "%s@%s" % (user, host)
        env.user = user
        env.sudo_user = user
        env.key_filename = key
        env.password = VM_IMAGE_ROOT_PASSWORD
        env.forward_agent = True
        env.use_shell = False
        env.prompts = {'[sudo] password for ' + user + ':': VM_IMAGE_ROOT_PASSWORD}

    @classmethod
    def call_remote_command(cls, command):
        """
        Executes remote command on virtual machine over ssh connection.
        @param command: command to execute.
        @return: result of command.
        """
        results_dict = cls.check_status(
            run(command,
                warn_only=True,
                stderr=sys.stderr,
                combine_stderr=True))

        return results_dict

    @classmethod
    def exec_task(cls, task):
        """
        Executes task on virtual machine over ssh connection.
        @param task: task name
        @return: result of task.
        """
        results_dict = execute(task)

        return results_dict

    @staticmethod
    def timeout(wait_time, loop_time, current_time):
        """
        Method to help with manipulate SSH timeout.
        @param wait_time: total time to wait.
        @param loop_time: time for sleep.
        @param current_time: actual time.
        @return: If actual time is greater then total time return false, if not return true.
        """
        if wait_time > current_time:
            time.sleep(loop_time)
            return False
        else:
            return True

    @staticmethod
    def check_status(result):
        """
        Check result and pass authorization privileges.
        @param result:
        @return:
        """
        if result.failed:
            raise Exception

        return result

    @classmethod
    def close_connection(cls):
        """
        Closes connection for ssh.
        """
        disconnect_all()

    @classmethod
    def check_juju_status(cls, application):
        """
        Checks installation status of given application.
        @param application: current installing application.
        @return: juju_instance if application is successfully started.
        """
        raw_json = cls.call_remote_command('juju status --format=json')

        try:
            status = json.loads(raw_json)
        except Exception, ex:
            error(None,
                  "During call 'juju status --format=json' except problem with obtain information from remote server"
                  + str(ex))

        services = status.get('services')
        machines = status.get('machines')

        if len(machines) <= 1:
            error(None, "Juju environment is bootstraped, no services deployed yet.")

        current_time = 0
        for name, service in services.iteritems():
            if service.get('units'):
                units = service['units']
                # unit_machines = ", ".join([u['machine'] for u in units.values()])
                # num_of_units = str(len(service['units'].values()))
                # open_ports = " ".join(
                #     [p.split('/')[0] for p in service['units']
                #         .values()[0]
                #         .get('open-ports', [])]
                # ) or "none"
                machine = machines[service['units'].values()[0]['machine']]
                agent_state = service['units'].values()[0].get('agent-state')
                public_address = service['units'].values()[0].get('public-address')
                instance_id = machine['instance-id']
                machine_number = units.values()[0]['machine']
                # exposed = "[exposed]" if service['exposed'] else ""
                # unit_plural = "s" if len(units) > 1 else ""
                # relations = ", ".join(service.get('relations', {}).keys())
                if name == application:
                    if agent_state == 'started':
                        juju_instance = JujuInstance()
                        juju_instance.name = name
                        juju_instance.units = units
                        # juju_instance.unit_machines = unit_machines
                        # juju_instance.num_of_units = num_of_units
                        # juju_instance.open_ports = open_ports
                        juju_instance.machine = machine
                        juju_instance.agent_state = agent_state
                        juju_instance.public_address = public_address
                        juju_instance.instance_id = instance_id
                        juju_instance.machine_number = machine_number
                        # juju_instance.exposed = exposed
                        # juju_instance.unit_plural = unit_plural
                        # juju_instance.relations = relations
                        return juju_instance
                    else:
                        current_time += LOOP_TIME
                        is_timeout = SSHConnector.timeout(WAIT_TIME, LOOP_TIME, current_time)
                        if is_timeout:
                            break
                        cls.check_juju_status(application)

        return None
