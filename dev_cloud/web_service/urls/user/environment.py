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
from django.conf.urls import patterns, url, include
from core.utils.decorators import user_permission, vm_permission
from web_service.views.user.enviroment import wizard_setup, generate_dependencies, customize_environment, \
    define_environment, summary, validation_process, validation_process_ip, validation_process_resources, \
    validation_process_ip_pre, view_environment, environments_list, get_vm_status, destroy_vm, refresh_vm_tasks, \
    show_vnc, get_cpu_load, get_ssh_key, view_predefined, customize_predefined_environment, \
    define_predefined_environment

main_patterns = patterns('web_service.views.user.enviroment',
                         url(r'^app/create/environment/$', user_permission(wizard_setup),
                             name='personalized_environment'),
                         url(r'^app/create/environment/technology/(?P<technology>\w+)/$',
                             user_permission(generate_dependencies),
                             name='generate_dependencies'),
                         url(
                             r'^app/create/environment/customize/(?P<technology>\w+)/(?P<application>[\w\-]+)/(?P<operation>\w+)/$',
                             user_permission(customize_environment), name='customize_environment'),
                         url(r'^app/create/environment/define/(?P<technology>\w+)/(?P<exposed_ip>\w+)/$',
                             user_permission(define_environment), name='define_environment'),
                         url(r'^app/create/environment/summary/$', user_permission(summary), name='summary'),
                         url(r'^app/create/environment/validation_process/(?P<template>\w+)/(?P<exposed_ip>\w+)/$',
                             user_permission(validation_process), name='validation_process'),
                         url(r'^app/create/environment/validation_process_ip/(?P<exposed_ip>\w+)/$',
                             user_permission(validation_process_ip), name='validation_process_ip'),
                         url(r'^app/create/environment/validation_process_ip_pre/(?P<exposed_ip>\w+)/$',
                             user_permission(validation_process_ip_pre), name='validation_process_ip_pre'),
                         url(r'^app/create/environment/validation_process_resources/(?P<template_id>\w+)/$',
                             user_permission(validation_process_resources), name='validation_process_resources'),
                         url(r'^app/environments/$', user_permission(environments_list), name='environments_list'),
                         url(r'^app/environments/(?P<destroy_status>\w+)/$', user_permission(environments_list),
                             name='environments_list'),
                         url(r'^app/environments/show_vm/(?P<vm_id>\w+)/$', vm_permission(view_environment),
                             name='view_environment'),
                         url(r'^app/environments/vm_status/(?P<vm_id>\w+)/$', vm_permission(get_vm_status),
                             name='get_vm_status'),
                         url(r'^app/environments/destroy/(?P<vm_id>\w+)/$', vm_permission(destroy_vm),
                             name='destroy_vm'),
                         url(r'^app/environments/refresh_tasks/(?P<vm_id>\w+)/$', vm_permission(refresh_vm_tasks),
                             name='refresh_vm_tasks'),
                         url(r'^app/environments/show_vm/vnc/(?P<vm_id>\w+)/$', vm_permission(show_vnc),
                             name='show_vnc'),
                         url(r'^app/environments/show_vm/cpu_load/(?P<vm_id>\w+)/$', vm_permission(get_cpu_load),
                             name='get_cpu_load'),
                         url(r'^app/environments/show_vm/get_ssh_key/(?P<vm_id>\w+)/$', vm_permission(get_ssh_key),
                             name='get_ssh_key'),
                         url(r'^app/create/environment/predefined/$', user_permission(view_predefined),
                             name='predefined_environment'),
                         url(
                             r'^app/create/environment/predefined/customize/(?P<application>[\w\-]+)/(?P<operation>\w+)/$',
                             user_permission(customize_predefined_environment),
                             name='customize_predefined_environment'),
                         url(
                             r'^app/create/environment/predefined/define/(?P<application>[\w\-]+)/(?P<exposed_ip>\w+)/$',
                             user_permission(define_predefined_environment),
                             name='define_predefined_environment'))

urlpatterns = patterns('', url(r'^main/', include(main_patterns)))
