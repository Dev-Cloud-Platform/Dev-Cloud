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
import time
import sys

from fabric.api import execute, run, env
from fabric.network import disconnect_all
from core.settings.config import VM_IMAGE_ROOT_PASSWORD


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
        disconnect_all()
