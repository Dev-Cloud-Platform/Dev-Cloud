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

import json
from newrelic.packages import requests
from core.settings import config

username = config.CLM_LOGIN
password = config.CLM_PASSWORD
adres_clm = config.CLM_ADDRESS

payload = {}

r = requests.post(adres_clm + '/guest/cluster/list_names/', data=json.dumps(payload))
print r.status_code
print r.text

for cluster in json.loads(r.text)['data']:
    print 'id:', cluster['cluster_id'], 'name:', cluster['name']

payload = {'login': username, 'password': password, 'cm_id': 1}
r = requests.post(adres_clm + '/user/key/get_list/', data=json.dumps(payload))
print r.status_code
print r.text