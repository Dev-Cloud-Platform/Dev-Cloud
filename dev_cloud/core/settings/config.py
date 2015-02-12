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

import logging

LOG_LEVEL = logging.DEBUG

LOG_DIR = '/var/log/DevCloud/'

DEV_CLOUD_DATA = {
    'site_domain': '192.245.169.169',   # Web interface address for activation link
    'site_name': 'Dev Cloud'            # System name in emails
}

AWS_ACCESS_KEY_ID = ''

AWS_SECRET_ACCESS_KEY = ''

CLM_LOGIN = ''

CLM_PASSWORD = ''

CLM_ADDRESS = 'http://www.cloud.ifj.edu.pl:8000/'

########## SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = '54tdc1@#%r8+(#s4s03w(26u8l7x*l=us(hfcgwn^xw6^-32rh'
########## END SECRET CONFIGURATION