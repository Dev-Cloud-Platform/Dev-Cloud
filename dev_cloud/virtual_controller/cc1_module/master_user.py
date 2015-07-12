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
from core.common import states
from core.common.states import STATUS, OK
from core.utils.log import error
from virtual_controller.cc1_module import address_clm, payload as payload_org, check_quota
from django.utils.translation import ugettext as _


class MasterUser(check_quota.Quota):
    """
    Class which represents master user (super user), which is set in config file.
    """

    @staticmethod
    def get_info_data():
        """
        Returns user's data.
        """
        payload = copy.deepcopy(payload_org)
        data = requests.post(address_clm + 'user/user/get_my_data/', data=json.dumps(payload))
        if data.status_code == 200 and ast.literal_eval(data.text).get(STATUS) == OK:
            return ast.literal_eval(data.text).get('data')
        else:
            error(None, _("CC1 - Problem with request: ") + data.url)

    @staticmethod
    def get_groups():
        payload = copy.deepcopy(payload_org)
        groups_id = requests.post(address_clm + 'user/group/list_own_groups/', data=json.dumps(payload))
        if groups_id.status_code == 200 and ast.literal_eval(groups_id.text).get(STATUS) == OK:
            return ast.literal_eval(groups_id.text).get('data')
        else:
            error(None, _("CC1 - Problem with request: ") + groups_id.url)

    @staticmethod
    def get_group_id():
        for group_id in MasterUser.get_groups():
            if group_id.get('name') == 'Dev Cloud':
                return group_id.get('group_id')

    @staticmethod
    def get_images_list():
        """
        Method returns list of images.
        @return: (list(dict)) images: {gid, name, [images]}
        """
        payload = copy.deepcopy(payload_org)
        payload['caller_id'] = MasterUser.get_info_data().get('user_id')
        payload['group_id'] = MasterUser.get_group_id()
        payload['access'] = states.image_access.get('private')
        images_list = requests.post(address_clm + 'user/system_image/get_list/', data=json.dumps(payload))
        if images_list.status_code == 200 and ast.literal_eval(images_list.text).get(STATUS) == OK:
            return ast.literal_eval(images_list.text).get('data')
        else:
            error(None, _("CC1 - Problem with request: ") + images_list.url)