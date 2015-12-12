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

from django.views.decorators.cache import never_cache
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django_ajax.decorators import ajax
from requests import ConnectionError

from core.common.states import OK, FAILED, UNKNOWN_ERROR, CM_ERROR, vm_states
from core.utils.auth import session_key
from core.utils.decorators import django_view, user_permission, vm_permission, update_environment
from core.utils.log import error
from core.utils.messager import get
from database.models.installed_applications import InstalledApplications
from database.models.template_instances import TemplateInstances
from database.models.virtual_machines import VirtualMachines
from database.models.vm_tasks import VmTasks
from virtual_controller.cc1_module.public_ip import NONE_AVAILABLE_PUBLIC_IP
from virtual_controller.juju_core.technology_builder import TechnologyBuilder, JAVA, PHP, NODEJS, RUBY, PYTHON
from web_service.forms.enviroment.create_vm import CreateVMForm
from web_service.views.user.user import generate_active

EXPOSE = 'expose'
UNEXPOSE = 'unexpose'


@django_view
@user_permission
def environments_list(request, destroy_status=None, template_name='app/environment/environments_list.html'):
    """
    Shows all virtual machines belong to user.
    @param request:
    @param destroy_status: Status of destroy machine, if was called.
    @param template_name: template to render.
    @return: view to render
    """
    return render_to_response(template_name,
                              dict({'destroy_status': destroy_status}.items() + generate_active('manage_env').items()),
                              context_instance=RequestContext(request))


@django_view
@vm_permission
def view_environment(request, vm_id, template_name='app/environment/view_environment.html'):
    """
    Shows selected virtual machine.
    @param request:
    @param vm_id: id of virtual machine.
    @param template_name: template to render.
    @return: view to render
    """
    selected_vm = vm_id
    installed_apps = InstalledApplications.objects.filter(virtual_machine__id=vm_id)
    workspace_name = installed_apps[0].workspace
    virtual_machine = VirtualMachines.objects.get(id=installed_apps[0].virtual_machine.id)
    used_template = TemplateInstances.objects.get(template_id=virtual_machine.template_instance.template_id)
    vm_tasks = VmTasks.objects.filter(vm__id=installed_apps[0].virtual_machine.id)

    return render_to_response(template_name,
                              dict({'selected_vm': selected_vm, 'workspace_name': workspace_name,
                                    'virtual_machine': virtual_machine,
                                    'used_template': used_template,
                                    'installed_apps': installed_apps,
                                    'vm_tasks': vm_tasks}.items() + generate_active(
                                  'manage_env').items()),
                              context_instance=RequestContext(request))


@ajax
@vm_permission
def get_vm_status(request, vm_id, template_name='app/environment/get_vm_status.html'):
    """
    Gets status of given virtual machine.
    @param request:
    @param vm_id: virtual machine id.
    @return: status of virtual machine.
    """
    try:
        vm_id = VirtualMachines.objects.get(id=vm_id).vm_id
        vm_status = vm_states.get(int(ast.literal_eval(
            get('virtual-machines/get-vm-status/?vm_id=%s' % str(vm_id), request_session=request).text)))

        return render_to_response(template_name, dict({'vm_status': vm_status}.items()),
                                  context_instance=RequestContext(request))
    except Exception, ex:
        error(int(request.session[session_key]), str(ex))


@ajax
@vm_permission
def refresh_vm_tasks(request, vm_id, template_name='app/environment/refresh_vm_tasks.html'):
    """
    Refresh virtual machine tasks'.
    @param request:
    @param vm_id: virtual machine id.
    @param template_name: template to render.
    @return: view to render.
    """
    try:
        vm_tasks = VmTasks.objects.filter(vm__id=vm_id).order_by('-task')
    except:
        vm_tasks = None

    return render_to_response(template_name, dict({'vm_tasks': vm_tasks}.items()),
                              context_instance=RequestContext(request))


@django_view
@vm_permission
def destroy_vm(request, vm_id):
    """
    Destroys selected virtual machine.
    @param request:
    @param vm_id: virtual machine id.
    @return: status after destroy virtual machine
    """
    return redirect('force_destroy_vm', vm_id=vm_id)


@django_view
@vm_permission
def force_destroy_vm(request, vm_id):
    """
    Force destroys selected virtual machine.
    @param request:
    @param vm_id: virtual machine id.
    @return: status after destroy virtual machine
    """
    # Dirty Solution
    try:
        vm_id = VirtualMachines.objects.get(id=vm_id).vm_id
        destroy_status = ast.literal_eval(
            get('virtual-machines/destroy-vm/?vm_id=%s' % str(vm_id), request_session=request).text)
        update_environment(request)
        return redirect('environments_list', destroy_status=destroy_status)
    except Exception, ex:
        error(int(request.session[session_key]), str(ex))
        update_environment(request)
        return redirect('environments_list', destroy_status=FAILED)


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
    if request.method == 'POST':
        # Do creating virtual machine
        create_vm = CreateVMForm(request)
        vm = ast.literal_eval(get('virtual-machines/create-vm/?applications=%s' % create_vm.get_applications()
                                  + '&template_id=%s' % create_vm.get_template()
                                  + '&workspace=%s' % create_vm.get_workspace()
                                  + '&public_ip=%s' % create_vm.get_public_ip()
                                  + '&disk_space=%s' % create_vm.get_disk_space(), request_session=request).text)

        return redirect('view_environment', vm_id=str(vm.get('id')))

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
def generate_dependencies(request, technology=None, template_name='app/environment/step_2.html'):
    """
    Generates dependencies for chosen technology.
    @param request:
    @param technology: selected technology.
    @param template_name: template to render.
    @return: view to render.
    """
    try:
        selected_applications = get_selected_applications(request, technology)
        technology_builder = TechnologyBuilder()
        available_technology = technology_builder.extracts(technology)

        return render_to_response(template_name,
                                  dict(available_technology.items() + generate_active('create_env_own').items()
                                       + {'selected_applications': selected_applications}.items()),
                                  context_instance=RequestContext(request))
    except Exception, ex:
        error(int(request.session[session_key]), str(ex))


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
    return ast.literal_eval(get('template-instances/').text)


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
    @return: view to render
    """
    list_application_details = {}
    selected_applications = get_selected_applications(request, technology)

    for selected_application in selected_applications:
        application_details = get('applications/get-application/?application=' + selected_application)
        if application_details.status_code == 200:
            list_application_details = dict(
                list_application_details.items() + {
                    selected_application: ast.literal_eval(application_details.text)}.items())
        else:
            error(request.session['user']['user_id'], "Problem with request: " + application_details.url)

    requirements = calculate_requirements(list_application_details)
    proposed_template = get_proper_template(requirements)

    exposed_status = None

    if exposed_ip == EXPOSE:
        # Check if is possible to obtain public ip.
        # After discussion with supervisor,
        # check possibility of obtain ip will be checked
        # after pass form to create vm.
        exposed_status = True

    if exposed_ip == UNEXPOSE:
        exposed_status = False

    return render_to_response(template_name,
                              dict({'requirements': requirements, 'template': proposed_template,
                                    'list_of_templates': get_list_of_templates(),
                                    'exposed_status': exposed_status}.items()),
                              context_instance=RequestContext(request))


@ajax
@user_permission
def summary(request, template_name='app/environment/step_4.html'):
    """
    Display summary for invoice.
    @param request:
    @param template_name: template to render
    @return: view to render
    """

    return render_to_response(template_name, dict({'exposed': request.session.get('publicIP')}.items()),
                              context_instance=RequestContext(request))


def validate_ip(request):
    status = FAILED
    obtained_ip = get('virtual-machines/obtain-ip/', request)

    if obtained_ip.status_code == 200:
        if obtained_ip.text.replace('"', '') != NONE_AVAILABLE_PUBLIC_IP \
                and obtained_ip.text.replace('"', '') != UNKNOWN_ERROR \
                and obtained_ip.text.replace('"', '') != CM_ERROR:
            get('virtual-machines/release-ip/?ip=%s' % obtained_ip.text.replace('"', ''), request)
            status = OK
    else:
        error(request.session['user']['user_id'], "Problem with request: " + obtained_ip.url)

    return status


def validate_resources(request, template_id):
    status = FAILED
    checked_resources = get('virtual-machines/resource-test/?template_id=%s' % template_id, request)

    if checked_resources.status_code == 200:
        status = OK
    else:
        error(request.session['user']['user_id'], "Problem with request: " + checked_resources.url)

    return status


@ajax
@csrf_protect
@user_permission
@never_cache
def validation_process_ip_pre(request, exposed_ip, template_name='app/environment/validation_ip_pre.html'):
    if exposed_ip == EXPOSE:
        return render_to_response(template_name, dict(), context_instance=RequestContext(request))


@ajax
@csrf_protect
@user_permission
@never_cache
def validation_process_ip(request, exposed_ip, template_name='app/environment/validation_ip.html'):
    if exposed_ip == EXPOSE:
        return render_to_response(template_name, dict({"validation_ip": validate_ip(request)}.items()),
                                  context_instance=RequestContext(request))


@ajax
@csrf_protect
@user_permission
@never_cache
def validation_process_resources(request, template_id, template_name='app/environment/validation_resources.html'):
    return render_to_response(template_name,
                              dict({"validation_resources": validate_resources(request, template_id)}.items()),
                              context_instance=RequestContext(request))


@ajax
@csrf_protect
@user_permission
@never_cache
def validation_process(request, template, exposed_ip, template_name='app/environment/validation_modal.html'):
    ip_to_validate = False
    if exposed_ip == EXPOSE:
        ip_to_validate = True

    return render_to_response(template_name,
                              dict({"ip_to_validate": ip_to_validate, "template_name": template}.items()),
                              context_instance=RequestContext(request))
