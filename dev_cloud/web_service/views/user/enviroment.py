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
import ast

import requests
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django_ajax.decorators import ajax
from core.settings import config
from core.utils.decorators import django_view, user_permission
from core.utils.log import error
from virtual_controller.juju_core.technology_builder import TechnologyBuilder, JAVA, PHP, NODEJS, RUBY, PYTHON
from web_service.views.user.user import generate_active


@django_view
@csrf_protect
@user_permission
def wizard_setup(request, template_name='app/environment/wizard_setup.html'):
    """
    Prepares properties for create new environment.
    @param request:
    @param template_name: template to render.
    @return: view to render.
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
    Generates dependencies for chosen technology.
    @param request:
    @param technology: selected technology.
    @param template_name: template to render.
    @return: view to render.
    """
    selected_applications = get_selected_applications(request, technology)
    technology_builder = TechnologyBuilder()
    available_technology = technology_builder.extracts(technology)

    return render_to_response(template_name,
                              dict(available_technology.items() + generate_active('create_env_own').items()
                                   + {'selected_applications': selected_applications}.items()),
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


def get_selected_applications(request, technology):
    """
    Gets selected applications from session for given technology.
    @param technology: selected technology.
    @return: selected applications for chosen technology.
    """
    selected_applications = []

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

    return selected_applications


def calculate_requirements(list_application_details):
    """
    Calculates requirements for virtual instance.
    @param list_application_details: the list with application and their details.
    @return: dict of requirements.
    """
    cpu = 0
    memory = 0
    space = 0

    for key, details in list_application_details.iteritems():
        cpu = max(cpu, int(details['cpu']))
        memory += int(details['memory'])
        space += int(details['space'])

    return dict({'cpu': cpu, 'memory': memory, 'space': space}.items())


def get_proper_template(requirements):
    """
    Gets proper template for given requirements.
    @param requirements: the dict of requirements.
    @return: proposal template for virtual instance.
    """
    list_of_templates = get_list_of_templates()

    for template in list_of_templates:
        if requirements['cpu'] <= template['cpu'] and requirements['memory'] <= (template['memory'] * 1024):
            proper_template = template
            break

    return proper_template


def get_list_of_templates():
    """
    Gets list of all available template for instances.
    @return: list of all available template for instances.
    """
    return ast.literal_eval(requests.get(config.REST_API_ADDRESS + 'rest_api/template-instances/').text)


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

    return get_selected_applications(request, technology)


@ajax
@user_permission
def define_environment(request, technology, exposed_ip, template_name='app/environment/step_3.html'):
    """

    @param request:
    @param technology: selected technology.
    @param template_name: template to render.
    @return:
    """
    list_application_details = {}
    selected_applications = get_selected_applications(request, technology)

    for selected_application in selected_applications:
        application_details = requests.get(config.REST_API_ADDRESS +
                                           'rest_api/applications/get-application/?application=' + selected_application)
        if application_details.status_code == 200:
            list_application_details = dict(
                list_application_details.items() + {
                    selected_application: ast.literal_eval(application_details.text)}.items())
        else:
            error(request.session['user']['user_id'], "Problem with request: " + application_details.url)

    requirements = calculate_requirements(list_application_details)
    proposed_template = get_proper_template(requirements)

    exposed_status = None

    if exposed_ip == 'expose':
        # Check if is possible to obtain public ip.
        exposed_status = True

    if exposed_ip == 'unexpose':
        exposed_status = False

    return render_to_response(template_name,
                              dict({'requirements': requirements, 'template': proposed_template,
                                    'list_of_templates': get_list_of_templates(), 'exposed_status': exposed_status}.items()),
                              context_instance=RequestContext(request))


@ajax
@user_permission
def summary(request, template_name='app/environment/step_4.html'):
    """

    @param request:
    @param template_name:
    @return:
    """

    return render_to_response(template_name, dict({'exposed': request.session.get('publicIP')}.items()),
                              context_instance=RequestContext(request))