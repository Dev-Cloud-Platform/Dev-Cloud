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

# Create your tests here.
import unittest
from teamcity import is_running_under_teamcity
from teamcity.unittestpy import TeamcityTestRunner
from dev_cloud.virtual_controller.juju_core.juju_instance import JujuInstance


class TestJujuInstance(unittest.TestCase):
    def testNone(self):
        juju_instance = JujuInstance()
        juju_instance.name = None
        self.assertEqual(juju_instance.name, None)

    def testString(self):
        juju_instance = JujuInstance()
        juju_instance.name = "test"
        self.assertEqual(juju_instance.name, 'test')


if __name__ == '__main__':
    if is_running_under_teamcity():
        runner = TeamcityTestRunner()
    else:
        runner = unittest.TextTestRunner()
    unittest.main(testRunner=runner)
