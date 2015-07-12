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
import requests
from rest_framework import status as status_code
from core.common.states import STATUS
from core.common.states import OK
from core.utils.log import error
from core.utils.messager import get
from virtual_controller.cc1_module import address_clm, payload as payload_org
from django.utils.translation import ugettext as _


class Quota(object):
    """
    Class represents object for quota.
    """

    user_id = None
    status = None

    def __init__(self, user_id):
        """
        Constructor for Quota object which assign basic properties such us user id.
        @param user_id: User id to set.
        """
        self.user_id = user_id

    def set_status(self, status):
        """
        Setter for status.
        @param status: Status about available resources.
        If code is equal 200 everything is OK, if 402 there are not enough resources.
        """
        self.status = status

    def get_status(self):
        """
        Getter for status.
        Gets value about check quotation.
        @return:  If code is equal 200 everything is OK, if 402 there are not enough resources.
        """
        return self.status

    def check_quota(self, template_id):
        """
        Sends request to check user quota's.
        @param template_id: selected id for template.
        @return:
        """
        payload = copy.deepcopy(payload_org)
        test = requests.post(address_clm + 'user/user/get_quota/', data=json.dumps(payload))

        if test.status_code == 200 and ast.literal_eval(test.text).get(STATUS) == OK:
            resource_status = ast.literal_eval(test.text)
            if self.__calculate_available_resources(self.__get_free_resources(resource_status.get('data')),
                                                    template_id):
                self.set_status(status_code.HTTP_200_OK)
            else:
                self.set_status(status_code.HTTP_402_PAYMENT_REQUIRED)
            return self.get_status()
        else:
            error(self.user_id, _("CC1 - Problem with request: ") + test.url)

    @staticmethod
    def __get_free_resources(data):
        """
        Gets free resources, based on given data.
        @param data: Data from CC1 about amount of used and free resources.
        @return: Calculated free resources.
        """
        free_resources = {'cpu': int(data.get('cpu')) - int(data.get('used_cpu')),
                          'memory': int(data.get('memory')) - int(data.get('used_memory')),
                          'storage': int(data.get('storage')) - int(data.get('used_storage')),
                          'public_ip': int(data.get('public_ip')) - int(data.get('used_public_ip'))}

        return free_resources

    @staticmethod
    def __calculate_available_resources(free_resources, template_id):
        """
        Calculates available resources for current template.
        @param free_resources: Dictionary with information about free resources.
        @param template_id: Id of template to create.
        @return: If True, enough resources, if False not enough resources.
        """
        is_available = True
        selected_template = ast.literal_eval(get('template-instances/get-template/?template_id=%s' % template_id).text)

        if int(free_resources.get('cpu')) - int(selected_template.get('cpu')) <= 0:
            is_available = False
            error(None, _('Not enough cpu cores'))

        if int(free_resources.get('memory')) - (int(selected_template.get('memory')) * 1000) <= 0:
            is_available = False
            error(None, _('Not enough free memory'))

        # TODO: Check also storage, and optional IP.

        return is_available