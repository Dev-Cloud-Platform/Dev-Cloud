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
from django.conf.urls import include, patterns, url
from core.utils.decorators import admin_permission
from web_service.views.admin.user import user_activation, ajax_activation_edit, ajax_activation_delete


main_patterns = patterns('web_service.views.user.user',
                         url(r'^app/user_activation/$', admin_permission(user_activation), name='user_activation'),
                         url(r'^app/user_activation/(?P<id>[0-9]+)/$', admin_permission(ajax_activation_edit),
                             name='ajax_activation_edit'))

urlpatterns = patterns('',
                       url(r'^main/', include(main_patterns)))