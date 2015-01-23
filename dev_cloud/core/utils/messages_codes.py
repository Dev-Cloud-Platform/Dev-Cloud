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
from django.template.defaultfilters import force_escape
from django.utils.translation import ugettext_lazy as _

auth_error_text = _('Authorization error. Re-login required.')


# \c errors - dictionary of the errors <b>informations' keys</b> and <b>information</b>
# (for error informations without parameters):
ERRORS = {
    'ok': _('No error'),
    }


def get_error(error_key):
    """
        If error with \c error_key exists, function returns it's message. Otherwise it returns "*Unknown error :(*" message.
    """
    return force_escape(ERRORS.get(error_key) or error_key)