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
from core.common.states import FAILED
from core.utils import celery
from core.utils.messager import get
from virtual_controller.juju_core.technology_builder import JAVA, PHP, RUBY, NODEJS, PYTHON, PREDEFINED


class CreateVMForm(object):
    """
    Class for <b>creating new virtual machine</b>.
    """

    applications = {}

    template = None

    workspace = ''

    public_ip = False

    disk_space = ''

    ssh_private_key = ''

    ssh_public_key = ''

    def __init__(self, request=None):
        """
        Constructor for creating Virtual Machine which assign passed properties from request.
        @param request: Optional value, with data from request.
        """
        if request:
            self.set_applications(self.__get_list_of_applications(request))
            self.set_template(ast.literal_eval(request.POST['template']).get('template_id'))
            self.set_workspace(request.POST['full_name'])
            self.set_public_ip(request.POST['public_ip'])
            self.set_disk_space('10000')  # For feature improve, assign by UI.

    def set_applications(self, applications):
        self.applications = applications

    def get_applications(self):
        return self.applications

    def set_template(self, template):
        self.template = template

    def get_template(self):
        return self.template

    def set_workspace(self, workspace):
        self.workspace = workspace

    def get_workspace(self):
        return self.workspace

    def set_public_ip(self, public_ip):
        self.public_ip = public_ip

    def get_public_ip(self):
        return self.public_ip

    def set_disk_space(self, disk_space):
        self.disk_space = disk_space

    def get_disk_space(self):
        return self.disk_space

    def set_ssh_private_key(self, private_key):
        self.ssh_private_key = private_key

    def get_ssh_private_key(self):
        return self.ssh_private_key

    def set_ssh_public_key(self, public_key):
        self.ssh_public_key = public_key

    def get_ssh_public_key(self):
        return self.ssh_public_key

    def generate_ssh(self, request):
        self.set_ssh_private_key(self.__generate_ssh(request))

    def is_valid(self, request):
        """
        This method valid the given request and set object class with given properties if is OK.
        @return: True if given request is proper, False if is not.
        """
        is_valid = True

        self.set_applications(request.DATA.get('applications', None) or request.query_params.get('applications', None))
        self.set_template(request.DATA.get('template_id', None) or request.query_params.get('template_id', None))
        self.set_workspace(request.DATA.get('workspace', None) or request.query_params.get('workspace', None))
        self.set_public_ip(request.DATA.get('public_ip', None) or request.query_params.get('public_ip', None))
        self.set_disk_space(request.DATA.get('disk_space', None) or request.query_params.get('disk_space', None))

        if self.get_applications() is None \
                or self.get_template() is None \
                or self.get_workspace() is None \
                or self.get_public_ip() is None \
                or self.get_disk_space() is None:
            is_valid = False

        if is_valid:
            self.generate_ssh(request)

        return is_valid

    @staticmethod
    def __get_list_of_applications(request):
        """
        Gets the applications on session and return a array.
        @return: List of applications.
        """
        global selected_applications
        technology = request.POST['radio1']

        if technology == JAVA:
            selected_applications = request.session.get(JAVA, [])

        if technology == PHP:
            selected_applications = request.session.get(PHP, [])

        if technology == RUBY:
            selected_applications = request.session.get(RUBY, [])

        if technology == NODEJS:
            selected_applications = request.session.get(NODEJS, [])

        if technology == PYTHON:
            selected_applications = request.session.get(PYTHON, [])

        if technology == PREDEFINED:
            selected_applications = request.session.get(PREDEFINED, [])

        return selected_applications

    def __generate_ssh(self, request):
        username = request.DATA.get('username', None) or request.query_params.get('username', None)
        password = request.DATA.get('password', None) or request.query_params.get('password', None)
        credentials = 'username=' + username + '&password=' + password

        key_name = "%s_%s_%s" % (username, self.get_workspace(), 'key')

        private = get('virtual-machines/generate-ssh-key/?key_name=%s' % key_name, credentials=credentials).text
        self.set_ssh_public_key(
            get('virtual-machines/get-ssh-key/?key_name=%s' % key_name, credentials=credentials).text)

        if private != FAILED:
            return private