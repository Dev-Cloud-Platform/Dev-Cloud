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


def release(ip_to_release):
    """
    Removes IP from callers public IP's pool and makes it available
    for other users to be further requested. Caller doesn't dispose this IP
    any more. He'll have to send another request if he needs more IPs.
    @param ip_to_release: Ip to release.
    """
    payload['public_ip_id'] = ip_to_release
    released_ip = requests.post(address_clm + '/user/public_ip/release/', data=json.dumps(payload))

    if released_ip.status_code == 200:
        return ast.literal_eval(released_ip.text)
    else:
        error("CC1 - Problem with request: " + released_ip.url)