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
from django.views.decorators.csrf import csrf_protect
from django_ajax.decorators import ajax
from core.utils.decorators import django_view
from core.utils.decorators import user_permission


@django_view
@user_permission
def app_view(request, template_name='app/main.html'):
    """
    View handling main app.
    @param request:
    @param template_name:
    @return:
    """
    if request.is_ajax():
        print "This is ajax"
    else:
        print "Not ajax"

    return render_to_response(template_name, context_instance=RequestContext(request))


@ajax
def ajax_test(request, template_name='app/main.html'):
    """
    Ajax test
    @param request:
    @return:
    """
    # if request.is_ajax():
    #     print "This is ajax"
    # else:
    #     print "Not ajax"

    return "karol4"
    # return render_to_response(template_name, context_instance=RequestContext(request))


@user_permission
@csrf_protect
def lock_screen(request, template_name='app/lock_screen.html'):
    """

    @param request:
    @param template_name:
    @return:
    """

    return render_to_response(template_name, context_instance=RequestContext(request))