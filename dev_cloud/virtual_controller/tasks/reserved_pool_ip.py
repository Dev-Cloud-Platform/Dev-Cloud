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
from __future__ import absolute_import
from core.utils.celery import app
from virtual_controller.cc1_module.public_ip import request as new_ip_request, get_list

poolIPList = []


class PoolIP(object):
    """
    Class represents pool for IP address.
    """
    public_ip_id = ""
    ip_address = ""

    @staticmethod
    def get_public_id(address_list, ip_address):
        return filter(lambda address: address["address"] == ip_address, address_list)[0].get("public_ip_id")

    def __init__(self):
        self.assign()

    def assign(self):
        ip_request = new_ip_request()
        if ip_request.get("status") == "ok":
            PoolIP.ip_address = ip_request.get("data")
            PoolIP.public_ip_id = PoolIP.get_public_id(get_list().get("data"), PoolIP.ip_address)

    def get_ip_adress(self):
        return PoolIP.ip_address

    def get_public_ip_id(self):
        return PoolIP.public_ip_id


@app.task(trail=True)
def request(i):
    """

    @return:
    """
    poolIP = PoolIP()
    poolIPList.append(poolIP)
    return release.delay(i)


@app.task(trail=True)
def release(i):
    """

    @return:
    """
    pass