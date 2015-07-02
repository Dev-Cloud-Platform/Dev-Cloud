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

from virtual_controller.juju_core.technology_builder import JAVA, PHP, RUBY, NODEJS, PYTHON


class CreateVMForm(object):
    """
    Class for <b>creating new virtual machine</b>.
    """

    applications = {}

    template = None

    workspace = ''

    public_ip = False

    disk_space = ''

    def __init__(self, request):
        """
        Constructor for creating Virtual Machine which assign passed properties from request.
        """
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

    @staticmethod
    def __get_list_of_applications(request):
        """
        Gets the applications on session and return a array.
        @return: List of applications.
        """
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

        return selected_applications
