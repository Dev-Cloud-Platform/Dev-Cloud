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
from core.utils.views import direct_to_template


account_patterns = patterns('web_service.views.user.user',
                            url(r'^$', user_permission(direct_to_template), {'template_name': 'account/base.html'}, name='acc_account'),
                            )


urlpatterns = patterns('',
                       url(r'^account/', include(account_patterns)),
                       )