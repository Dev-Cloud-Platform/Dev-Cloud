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


import re

from django.conf import settings
from core.utils.views import make_request


SHA1_RE = re.compile('^[A-Z0-9]{40}$')


def register(**kwargs):
    """
        Method turns keyword arguments (which describe user) into a dictionary and registers the user by \c XMLRPC and
    """
    if ('recaptcha' in kwargs):
        kwargs.pop('recaptcha')
    kwargs['wi_data'] = settings.WI_DATA
    return make_request('guest/user/register/', kwargs)


def activate(activation_key):
    """
        Method checks, if \c activation_key is ok. If so, it activates user.
    """
    if SHA1_RE.search(activation_key):
        response = make_request('guest/user/activate/', {'act_key': activation_key, 'wi_data': settings.WI_DATA})
        if response['status'] == 'ok':
            return response
    return False