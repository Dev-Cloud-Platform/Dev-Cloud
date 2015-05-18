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
from datetime import datetime, timedelta
from core.utils.celery import app
from core.utils.log import info
from virtual_controller.cc1_module.public_ip import request as new_ip_request, get_list, release as ip_release

poolIPList = []


class PoolIP(object):
    """
    Class represents pool for IP address.
    """
    public_ip_id = ""
    ip_address = ""
    user_id = ""

    @staticmethod
    def get_public_id(address_list, ip_address):
        return filter(lambda address: address["address"] == ip_address, address_list)[0].get("public_ip_id")

    def __init__(self, user_id):
        self.assign(user_id)

    def assign(self, user_id):
        ip_request = new_ip_request()
        if ip_request.get("status") == "ok":
            self.ip_address = ip_request.get("data")
            self.public_ip_id = self.get_public_id(get_list().get("data"), self.ip_address)
            self.user_id = user_id
            info(user_id, "Assigned IP:" + self.get_ip_address())

    def remove(self):
        ip_release(self.get_public_ip_id())
        info(self.user_id, "Release IP:" + self.get_ip_address())

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


@app.task(trail=True, name='tasks.request')
def request(user_id):
    """
    Method to obtain public IP form CC1.
    @return:
    """
    poolIP = PoolIP(user_id)
    poolIPList.append(poolIP)
    return release.apply_async(args=(poolIP.dict,), eta=datetime.now() + timedelta(minutes=1), serializer='json')


@app.task(trail=True, name='tasks.release')
def release(poolIP):
    """
    Method to release public IP form CC1.
    @return:
    """
    poolIP.remove()
    poolIPList.remove(poolIP)
