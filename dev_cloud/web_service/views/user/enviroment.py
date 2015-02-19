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
from virtual_controller.juju_core.technology_builder import TechnologyBuilder, JAVA, PHP, NODEJS, RUBY, PYTHON
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
    request.session[JAVA] = []
    request.session[PHP] = []
    request.session[RUBY] = []
    request.session[NODEJS] = []
    request.session[PYTHON] = []

    return render_to_response(template_name,
                              dict(generate_active('create_env_own').items()),
                              context_instance=RequestContext(request))


@ajax
@user_permission
def generate_dependencies(request, technology, template_name='app/environment/step_2.html'):
    """

    @param request:
    @param technology:
    @param template_name:
    @return:
    """
    selected_applications = []
    technology_builder = TechnologyBuilder()
    available_technology = technology_builder.extracts(technology)

    if technology == JAVA:
        selected_applications = request.session.get(JAVA, [])

    if technology == PHP:
        selected_applications = request.session.get(PHP, [])

    if technology == RUBY:
        selected_applications = request.session.get(RUBY, [])

    if technology == NODEJS:
        selected_applications = request.session.get(NODEJS, [])

    if technology == PYTHON:
        selected_applications = request.session.get(PYTHON, [])

    print {'selected_applications': selected_applications}

    return render_to_response(template_name,
                              dict(available_technology.items() + generate_active('create_env_own').items() + {
                                  'selected_applications': selected_applications}.items()),
                              context_instance=RequestContext(request))


def update_application(array, application, operation):
    """
    Adds or remove application for given array.
    @param array: list of applications.
    @param application: application to add or to remove.
    @param operation: string with command if contains remove then removes, or add then adds.
    """
    if operation == 'add':
        if not array.__contains__(application):
            array.append(application)

    if operation == 'remove':
        array.remove(application)


@ajax
@user_permission
def customize_environment(request, technology, application, operation):
    """
    Customizes environment.
    @param request:
    @param application: application to add or to remove.
    @param operation: string with command if contains remove then removes, or add then adds.
    @return:
    """

    if technology == JAVA:
        update_application(request.session.get(JAVA, []), application, operation)

    if technology == PHP:
        update_application(request.session.get(PHP, []), application, operation)

    if technology == RUBY:
        update_application(request.session.get(RUBY, []), application, operation)

    if technology == NODEJS:
        update_application(request.session.get(NODEJS, []), application, operation)

    if technology == PYTHON:
        update_application(request.session.get(PYTHON, []), application, operation)

