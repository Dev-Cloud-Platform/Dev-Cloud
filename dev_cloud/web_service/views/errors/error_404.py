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
from django.shortcuts import render_to_response
from django.template import RequestContext
from core.utils.auth import session_key
from database.models import Users


def bad_request(request, template_name='404.html'):
    """
    404 error handler.
    @param request:
    @param template_name: 404.html
    @return:
    """
    try:
        user = Users.objects.get(id=int(request.session[session_key]))
    except Exception:
        user = None

    if user:
        template_name = '404_logged.html'

    return render_to_response(template_name, context_instance=RequestContext(request))