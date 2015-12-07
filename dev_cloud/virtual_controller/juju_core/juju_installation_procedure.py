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

import sys

from fabric.api import run, task, sudo
from virtual_controller.juju_core.ssh_connector import SSHConnector

sys.stderr = open('/dev/null')
sys.stderr = sys.__stderr__


@task
def init_juju_on_vm():
    """
    Exec procedure on remote server to initialize juju environment.
    """
    SSHConnector.check_status(
        run('juju generate-config && juju switch local',
            warn_only=True,
            stderr=sys.stderr,
            combine_stderr=True)
    )

    SSHConnector.check_status(
        sudo('chmod 777 /home/devcloud/.juju/ -R',
             shell=True,
             warn_only=True,
             stderr=sys.stderr,
             combine_stderr=True)
    )

    SSHConnector.check_status(
        run('juju bootstrap',
            warn_only=True,
            stderr=sys.stderr,
            combine_stderr=True)
    )
