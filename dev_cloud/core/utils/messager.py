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
from django.core.exceptions import ObjectDoesNotExist
import requests
from core.settings import config
from core.utils.auth import session_key
from database.models import Users

API_ADDRESS = config.REST_API_ADDRESS + 'rest_api/'


def get(url, request_session=None, credentials=None):
    """
    Method create request get for Dev Cloud API.
    @param url: request url to call.
    @param request_session: request session to obtain user credentials.
    @param credentials: credentials to authorization.
    @return: status code.
    """
    if request_session:
        try:
            user = Users.objects.get(id=int(request_session.session[session_key]))
            credentials = 'username=' + user.login + '&password=' + user.password
        except ObjectDoesNotExist:
            credentials = None

    return requests.get(API_ADDRESS + url, params=credentials)


def post(url, request_session=None, credentials=None, data=None):
    """
    TODO: Not working properly. TO FIX!
    Method create post request for Dev Cloud API
    @param url: request url to call.
    @param request_session: request session to obtain user credentials.
    @param credentials: credentials to authorization.
    @return: status code.
    """
    if request_session:
        try:
            user = Users.objects.get(id=int(request_session.session[session_key]))
            credentials = 'username=' + user.login + '&password=' + user.password
        except ObjectDoesNotExist:
            credentials = None

    return requests.post(API_ADDRESS + url, data=json.dumps(data))