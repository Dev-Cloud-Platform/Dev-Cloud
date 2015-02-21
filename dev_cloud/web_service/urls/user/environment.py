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
from core.utils.decorators import user_permission
from web_service.views.user.enviroment import wizard_setup, generate_dependencies, customize_environment, \
    define_environment

main_patterns = patterns('web_service.views.user.enviroment',
                         url(r'^app/create/environment/$', user_permission(wizard_setup),
                             name='personalized_environment'),
                         url(r'^app/create/environment/technology/(?P<technology>\w+)/$',
                             user_permission(generate_dependencies),
                             name='generate_dependencies'),
                         url(
                             r'^app/create/environment/customize/(?P<technology>\w+)/(?P<application>[\w\-]+)/(?P<operation>\w+)/$',
                             user_permission(customize_environment), name='customize_environment'),
                         url(r'^app/create/environment/define/(?P<technology>\w+)/$',
                             user_permission(define_environment), name='define_environment'))

urlpatterns = patterns('',
                       url(r'^main/', include(main_patterns)))