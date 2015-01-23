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

auth_patterns = patterns('web_service.views.guest.user',
                         url(r'^login/$', 'login', name='login'),
                         url(r'^logout/$', 'logout', name='logout'),
                         )


main_patterns = patterns('web_service.views.guest.user',
                         url(r'^change_language/(?P<lang>\w+)/$', 'change_language', name='change_language'),
                         )


help_patterns = patterns('web_service.views.guest.user',
                         url(r'^$', 'hlp_help', name='hlp_help'),
                         )


urlpatterns = patterns('',
                       url(r'^auth/', include(auth_patterns)),
                       url(r'', include(main_patterns)),
                       # url(r'^account/', include(account_patterns)),
                       url(r'^help/', include(help_patterns)),
                       # url(r'^registration/', include(registration_patterns)),
                       )