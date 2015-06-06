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
from core.utils.log import error, info
from virtual_controller.cc1_module import address_clm, payload
from django.utils.translation import ugettext as _


NONE_AVAILABLE_PUBLIC_IP = _("None available public IP")


class PoolIP(object):
    """
    Class represents pool for IP address.
    """
    public_ip_id = ""
    ip_address = ""
    user_id = ""

    @staticmethod
    def get_public_id_for_ip(ip_address):
        return filter(lambda address: address["address"] == ip_address, get_list().get("data"))[0].get("public_ip_id")

    def __init__(self, user_id, ip_address=None):
        self.user_id = user_id
        if ip_address is not None:
            self.set_ip_address(ip_address)
            self.set_public_ip_id(self.get_public_id_for_ip(self.get_ip_address()))

    def assign(self):
        ip_request = request()
        if ip_request.get("status") == "ok":
            self.ip_address = ip_request.get("data")
            self.public_ip_id = self.get_public_id_for_ip(self.ip_address)
            info(self.user_id, "Assigned IP:" + self.get_ip_address())

    def remove(self):
        release(self.get_public_ip_id())
        info(self.user_id, "Release IP:" + self.get_ip_address())

    def set_public_ip_id(self, public_ip_id):
        self.public_ip_id = public_ip_id

    def set_ip_address(self, ip_address):
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


def get_list():
    """
    Returns list of caller's public IPs.
    """
    ip_list = requests.post(address_clm + '/user/public_ip/get_list/', data=json.dumps(payload))

    if ip_list.status_code == 200:
        return ast.literal_eval(ip_list.text)
    else:
        error("CC1 - Problem with request: " + ip_list.url)


def request():
    """
    Sends request to grant new public IP for caller. If caller's quota allows,
    user will obtain new public IP.
    """
    new_ip = requests.post(address_clm + '/user/public_ip/request/', data=json.dumps(payload))

    if new_ip.status_code == 200:
        return ast.literal_eval(new_ip.text)
    else:
        error("CC1 - Problem with request: " + new_ip.url)


def assign():
    """
    Assigns public IP to caller's VM with given id.
    """
    pass


def unassign():
    """
    Unassigned public IP from VM with given id. Unassigned public IP may be assigned
    to any of his VMs.
    """
    pass


def release(ip_id_to_release):
    """
    Removes IP from callers public IP's pool and makes it available
    for other users to be further requested. Caller doesn't dispose this IP
    any more. He'll have to send another request if he needs more IPs.
    @param ip_id_to_release: Ip id to release.
    """
    payload['public_ip_id'] = ip_id_to_release
    released_ip = requests.post(address_clm + '/user/public_ip/release/', data=json.dumps(payload))

    if released_ip.status_code == 200:
        pass
    else:
        error("CC1 - Problem with request: " + released_ip.url)