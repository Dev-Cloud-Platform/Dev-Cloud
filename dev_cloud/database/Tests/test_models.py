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

import unittest

from teamcity import is_running_under_teamcity
from teamcity.unittestpy import TeamcityTestRunner

from dev_cloud.database.models.applications import Applications
from dev_cloud.database.models.installed_applications import InstalledApplications
from dev_cloud.database.models.template_instances import TemplateInstances
from dev_cloud.database.models.virtual_machines import VirtualMachines


class ApplicationTestCase(unittest.TestCase):
    def test_model_application(self):
        instance = Applications(application_name="application_test")
        self.assertTrue(instance)

    def test_model_template_instance(self):
        instance = TemplateInstances(template_name="template_test")
        self.assertTrue(instance)

    def test_model_virtual_machine(self):
        example_instance = TemplateInstances(template_name="template_test")
        instance = VirtualMachines(template_instance=example_instance)
        self.assertTrue(instance)

    def test_model_installed_aplication(self):
        example_app = Applications(application_name="application_test")
        example_instance = TemplateInstances(template_name="template_test")
        example_virtual_machine = VirtualMachines(template_instance=example_instance)
        instance = InstalledApplications(workspace="test_workspace", application=example_app,
                                         virtual_machine=example_virtual_machine)
        self.assertTrue(instance)


if __name__ == '__main__':
    if is_running_under_teamcity():
        runner = TeamcityTestRunner()
    else:
        runner = unittest.TextTestRunner()
    unittest.main(testRunner=runner)