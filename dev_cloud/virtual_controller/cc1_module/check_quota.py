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
import json
import requests
from core.utils.log import error
from virtual_controller.cc1_module import address_clm, payload


class Quota(object):
    """
    Class represents object for quota.
    """

    user_id = ""
    status = ""

    def __init__(self, user_id):
        self.user_id = user_id

    def set_status(self, status):
        self.status = status

    def get_status(self):
        return self.status

    def check_quota(self, template_id):
        """
        Sends request to check user quota's.
        @param template_id: selected id for template.
        @return:
        """
        test = requests.post(address_clm + 'user/user/get_quota/', data=json.dumps(payload))

        if test.status_code == 200:
            self.set_status(ast.literal_eval(test.text))
            return self.get_status()
        else:
            error(self.user_id, "CC1 - Problem with request: " + test.url)