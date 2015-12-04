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
from fabric.api import run, runs_once, sudo, task
import sys


@task
@runs_once
def init_juju_on_vm():
    """
    Exec procedure on remote server to initialize juju environment.
    """
    print sudo('w', stderr=sys.stdout)
    # run('juju generate-config', shell=False)
    # run('juju switch local', shell=False)
    # sudo('juju bootstrap', shell=False, user='devcloud')