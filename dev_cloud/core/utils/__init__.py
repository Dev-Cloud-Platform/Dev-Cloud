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
from exception import RestErrorException
from messages_codes import get_error

REDIRECT_FIELD_NAME = 'next'

def check_response_errors(response, session):
    """
        Checks status of response response and throws appropriate error.
    """
    if response['status'] != 'ok':
        from dev_cloud.core.utils.auth import logout
        error_code = response['status']
        error_msg = get_error(error_code)
        raise RestErrorException(error_msg)

    return response
