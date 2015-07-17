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
from django.utils.translation import ugettext as _

FAILED = _('failed')

OK = 'ok'
STATUS = 'status'
DATA = 'data'
CM_ERROR = 'cm_error'
UNKNOWN_ERROR = 'Unknown error'
PUBLIC_IP_LIMIT = 'public_lease_limit'

vm_states = {
    0: _('init'),
    1: _('running'),
    2: _('closing'),
    3: _('closed'),
    4: _('saving'),
    5: _('failed'),
    6: _('saving failed'),
    7: _('running ctx'),
    8: _('restart'),
    9: _('suspend'),
    10: _('turned off'),
    11: _('erased'),
    12: _('erasing')
}

user_active_states = {
    'inactive': 0,
    'email_confirmed': 1,
    'ok': 2,
    'blocked': 3
}

registration_states = {
    'completed': 0,
    'mail_confirmation': 1,
    'admin_confirmation': 2,
    'error': 3,
    'disallowed': 4
}

image_access = {
    'private': 0,
    'public': 1,
    'group': 2
}