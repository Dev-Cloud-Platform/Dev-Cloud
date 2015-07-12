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
from core.common.states import OK, STATUS, CM_ERROR, PUBLIC_IP_LIMIT
from core.utils.log import error, info
from virtual_controller.cc1_module import address_clm, payload as payload_org
from django.utils.translation import ugettext as _


NONE_AVAILABLE_PUBLIC_IP = _("None available public IP")


class PoolIP(object):
    """
    Class represents pool for IP address.
    """
    public_ip_id = None
    ip_address = None
    user_id = None

    def __init__(self, user_id, ip_address=None):
        """
        Constructor for PoolIP which assign basic properties.
        @param user_id: Id of caller
        @param ip_address: Optional argument, to assign ip address if is existing.
        """
        self.user_id = user_id
        if ip_address is not None:
            self.set_ip_address(ip_address)
            self.set_public_ip_id(self.get_public_id_for_ip(self.get_ip_address()))

    def get_public_id_for_ip(self, ip_address):
        """
        Gets public id from CC1 pool for given IP.
        @param ip_address: IP address to find in CC1 IP pool.
        @return: Public id for given IP.
        """
        try:
            return filter(lambda address: address["address"] == ip_address, self.__get_list().get("data"))[0].get(
                "public_ip_id")
        except IndexError:
            error(self.user_id, _("Given IP not found on CC1"))

    def request(self):
        """
        Method requests new IP from CC1.
        @return: Status about request new IP.
        """
        ip_request = self.__request()
        if ip_request.get(STATUS) == OK:
            self.ip_address = ip_request.get("data")
            self.public_ip_id = self.get_public_id_for_ip(self.ip_address)
            info(self.user_id, _("Requested new IP:") + self.get_ip_address())
        elif ip_request.get(STATUS) == PUBLIC_IP_LIMIT:
            info(self.user_id, _("Public IP limit exceeded."))
        elif ip_request.get(STATUS) == CM_ERROR:
            error(self.user_id, _("Impossible to request new IP."))
        else:
            error(self.user_id, _("Unknown error."))

        return ip_request.get(STATUS)

    def remove(self):
        """
        Removes requested IP from CC1.
        @return:
        """
        release_request = self.__release(self.get_public_ip_id())
        if release_request.get(STATUS) == OK:
            info(self.user_id, _("Release IP:") + self.get_ip_address())
        elif release_request.get(STATUS) == CM_ERROR:
            error(self.user_id, _("Impossible to release " + self.get_ip_address()))
        else:
            error(self.user_id, _("Unknown error."))

        return release_request.get(STATUS)

    def set_public_ip_id(self, public_ip_id):
        """
        Setter for id of public IP.
        @param public_ip_id: Id of public IP to set.
        """
        self.public_ip_id = public_ip_id

    def set_ip_address(self, ip_address):
        """
        Setter for
        @param ip_address:
        @return:
        """
        self.ip_address = ip_address

    def get_ip_address(self):
        return self.ip_address

    def get_public_ip_id(self):
        return self.public_ip_id

    @property
    def dict(self):
        """
        @returns{dict} dictionary of PoolIP class
        \n fields:
        @dictkey{public_ip_id,int} id of ip address
        @dictkey{ip_address,string} ip address
        @dictkey{user_id,int} user id
        """
        d = {'public_ip_id': self.public_ip_id, 'ip_address': self.ip_address, 'user_id': self.user_id}
        return d

    @staticmethod
    def __get_list():
        """
        Returns list of caller's public IPs.
        """
        payload = copy.deepcopy(payload_org)
        ip_list = requests.post(address_clm + '/user/public_ip/get_list/', data=json.dumps(payload))

        if ip_list.status_code == 200 and ast.literal_eval(ip_list.text).get(STATUS) == OK:
            return ast.literal_eval(ip_list.text)
        else:
            error(None, _("CC1 - Problem with request: ") + ip_list.url)

    @staticmethod
    def __request():
        """
        Sends request to grant new public IP for caller. If caller's quota allows,
        user will obtain new public IP.
        """
        payload = copy.deepcopy(payload_org)
        new_ip = requests.post(address_clm + 'user/public_ip/request/', data=json.dumps(payload))

        if new_ip.status_code == 200 and ast.literal_eval(new_ip.text).get(STATUS) == OK:
            return ast.literal_eval(new_ip.text)
        else:
            error(None, _("CC1 - Problem with request: ") + new_ip.url)

    @staticmethod
    def __assign():
        """
        Assigns public IP to caller's VM with given id.
        """
        pass

    @staticmethod
    def __unassign():
        """
        Unassigned public IP from VM with given id. Unassigned public IP may be assigned
        to any of his VMs.
        """
        pass

    @staticmethod
    def __release(ip_id_to_release):
        """
        Removes IP from callers public IP's pool and makes it available
        for other users to be further requested. Caller doesn't dispose this IP
        any more. He'll have to send another request if he needs more IPs.
        @param ip_id_to_release: Ip id to release.
        """
        payload = copy.deepcopy(payload_org)
        payload['public_ip_id'] = ip_id_to_release
        released_ip = requests.post(address_clm + '/user/public_ip/release/', data=json.dumps(payload))

        if released_ip.status_code == 200 and ast.literal_eval(released_ip.text).get(STATUS) == OK:
            return json.loads(released_ip.text)
        else:
            error(None, _("CC1 - Problem with request: ") + released_ip.url)