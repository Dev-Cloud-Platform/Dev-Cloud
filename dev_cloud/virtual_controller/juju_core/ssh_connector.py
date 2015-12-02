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

from fabric import tasks
from fabric.api import env
from fabric.network import disconnect_all
from fabric.operations import sudo
from fabric.utils import abort
from core.settings.config import VM_IMAGE_ROOT_PASSWORD


class SSHConnector(object):
    """
    Class responsible for provide secure connection between dev cloud app and client virtual machine.
    """

    def __init__(self, host, user, key):
        env.host_string = "%s@%s" % (user, host)
        env.user = user
        env.key_filename = key
        env.password = VM_IMAGE_ROOT_PASSWORD

    @classmethod
    def call_remote_command(cls, command):
        """
        Executes remote command on virtual machine over ssh connection.
        @param command: command to execute.
        @return: result of command.
        """
        results_dict = tasks.execute(command)
        if results_dict.failed:
            abort("Aborting remote command")

        disconnect_all()
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
