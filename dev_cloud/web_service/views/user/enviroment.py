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
from core.utils.decorators import django_view, user_permission
from virtual_controller.juju_core.technology_builder import TechnologyBuilder
from web_service.views.user.user import generate_active


@django_view
@csrf_protect
@user_permission
def wizard_setup(request, template_name='app/environment/wizard_setup.html'):
    """

    @param request:
    @param template_name:
    @return:
    """

    return render_to_response(template_name,
                              dict(generate_active('create_env_own').items()),
                              context_instance=RequestContext(request))


@ajax
@user_permission
def generate_dependencies(request, technology, template_name=''):
    """

    @param request:
    @param technology:
    @param template_name:
    @return:
    """
    technology_builder = TechnologyBuilder()
    available_technology = technology_builder.extracts(technology)

    print available_technology

    return available_technology