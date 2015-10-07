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

from fabric import tasks
from fabric.api import env
from fabric.api import run
from fabric.network import disconnect_all


class SSHConnector(object):


    """
    Class responsible for provide secure connection between dev cloud app and client virtual machine.
    """

    def __init__(self, host, user, key):
        env.hosts = [host]
        env.user = [user]
        env.key = key

    @classmethod
    def call_remote_command(cls, command):
        """
        Executes remote command on virtual machine over ssh connection.
        @param command: command to execute.
        @return: result of command.
        """
        results_dict = tasks.execute(run(command))
        disconnect_all()
        return results_dict