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
import copy
import json
import time
import datetime
import requests
from core.common.states import STATUS, OK, DATA, FAILED, SSH_ALREADY_EXIST
from virtual_controller.cc1_module import address_clm, payload as payload_org
from virtual_controller.cc1_module.logger import error


class Key(object):
    """
    Class responsible for provide security safeties.
    """

    user_id = None
    name = None

    def __init__(self, user_id, name=None):
        """
        Constructor for Key class which assign basic properties.
        @param user_id: Id of caller
        @param name: Optional argument, which assign name for key.
        """
        self.user_id = user_id
        self.name = name

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def generate(self, name=None):
        """
        Generates SSH key pair.
        @return: Private part of the key.
        """
        if name is not None:
            self.set_name(name)

        payload = copy.deepcopy(payload_org)
        payload['name'] = self.get_name()

        private = requests.post(address_clm + 'user/key/generate/', data=json.dumps(payload))

        if private.status_code == 200 and ast.literal_eval(private.text).get(STATUS) == OK:
            return ast.literal_eval(private.text).get(DATA)
        elif private.status_code == 200 and ast.literal_eval(private.text).get(STATUS) == SSH_ALREADY_EXIST:
            timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            self.generate(self.get_name() + str(timestamp))
        else:
            error(self.user_id, private)
            return FAILED