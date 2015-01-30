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

from django.http.response import HttpResponse

from django.utils.translation import ugettext as _

from core.utils import RestErrorException


def success(message, status=0):
    """
    Returns json encoded ajax response.
    @param message:
    @param status:
    @return:
    """
    return HttpResponse(content=json.dumps({'status': status, 'data': message}), content_type="application/json")


def error(message):
    """
    Returns json encoded ajax response (error).
    @param message:
    @return:
    """
    return success(message, status=8000)


def success_with_key(message, filename, name, status=0):
    """
    Returns json encoded ajax response containing a file.
    @param message:
    @param filename:
    @param name:
    @param status:
    @return:
    """
    return HttpResponse(content=json.dumps({'status': status, 'data': message, 'file': filename, 'name': name}), content_type="application/json")


def ajax_request(view_func):
    """
    Decorator checking whether request is an AJAX request.
    @param view_func:
    @return:
    """
    def wrap(request, *args, **kwds):
        """
        Returned decorated function.
        @param request:
        @param args:
        @param kwds:
        @return:
        """
        if not request.is_ajax():
            return error(_('Not AJAX request!'))
        try:
            return view_func(request, *args, **kwds)
        except RestErrorException as ex:
            return error(ex.value)
    return wrap