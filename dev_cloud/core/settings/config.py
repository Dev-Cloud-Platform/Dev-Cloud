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

# Log format for each entry
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

DEV_CLOUD_IP_ADDRESS = '192.245.169.169'

DEV_CLOUD_DATA = {
    'site_domain': DEV_CLOUD_IP_ADDRESS,  # Web interface address for activation link
    'site_name': 'Dev Cloud'              # System name in emails
}

AWS_ACCESS_KEY_ID = 'm4gik'

AWS_SECRET_ACCESS_KEY = 'a4b53201134d95f4b817da90dd6bfc2e0b544470'

CLM_LOGIN = 'm4gik'

CLM_PASSWORD = 'a4b53201134d95f4b817da90dd6bfc2e0b544470'

CLM_ADDRESS = 'http://www.cloud.ifj.edu.pl:8000/'

# REST_API_ADDRESS = 'http://' + DEV_CLOUD_IP_ADDRESS + '/'
REST_API_ADDRESS = 'http://127.0.0.1/'

CELERY_IP_ADDRESS = '127.0.0.1'

########## SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = '54tdc1@#%r8+(#s4s03w(26u8l7x*l=us(hfcgwn^xw6^-32rh'
########## END SECRET CONFIGURATION