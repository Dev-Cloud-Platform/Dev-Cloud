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

from core.utils.views import direct_to_template
from web_service.views.guest.user import reg_activate, reg_register


auth_patterns = patterns('web_service.views.guest.user',
                         url(r'^login/$', 'login', name='login'),
                         url(r'^logout/$', 'logout', name='logout'))

main_patterns = patterns('web_service.views.guest.user',
                         url(r'^change_language/(?P<lang>\w+)/$', 'change_language', name='change_language'))

account_patterns = patterns('web_service.views.guest.user',
                            url(r'^password_reset/$', 'password_reset', name='password_reset'),
                            url(r'^password_reset_error/$', direct_to_template,
                                {'template_name': 'account/password_reset_error_email.html'},
                                name='password_reset_error'),
                            url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'acc_password_reset_confirm',
                                name='password_reset_confirm'))

help_patterns = patterns('web_service.views.guest.user',
                         url(r'^$', 'contact', name='contact'))

registration_patterns = patterns('web_service.views.guest.user',
                                 # Activation keys get matched by \w+ instead of the more specific
                                 # [a-fA-F0-9]{40} because a bad activation key should still get to the view;
                                 # that way it can return a sensible "invalid key" message instead of a
                                 # confusing 404.
                                 url(r'^activate/key/(?P<activation_key>\w+)/$', reg_activate, name='reg_activate'),
                                 url(r'^register/$', reg_register, name='reg_register'),
                                 url(r'^register/closed/$', direct_to_template,
                                     {'template_name': 'registration/registration_closed.html'}, name='reg_disallowed'),
                                 url(r'^register/completed/$', direct_to_template,
                                     {'template_name': 'registration/registration_completed.html'},
                                     name='registration_completed'),
                                 url(r'^register/mail_confirmation/$', direct_to_template,
                                     {'template_name': 'registration/registration_mail_confirmation.html'},
                                     name='registration_mail_confirmation'),
                                 url(r'^register/error/$', direct_to_template,
                                     {'template_name': 'registration/registration_error.html'},
                                     name='registration_error'),
                                 url(r'^activate/completed/$', direct_to_template,
                                     {'template_name': 'registration/activation_completed.html'},
                                     name='activation_completed'),
                                 url(r'^activate/admin_confirmation/$', direct_to_template,
                                     {'template_name': 'registration/activation_admin_confirmation.html'},
                                     name='activation_admin_confirmation'),
                                 url(r'^activate/error/$', direct_to_template,
                                     {'template_name': 'registration/activation_error.html'}, name='activation_error'))

urlpatterns = patterns('',
                       url(r'^auth/', include(auth_patterns)),
                       url(r'', include(main_patterns)),
                       url(r'^account/', include(account_patterns)),  # For reset password
                       url(r'^help/', include(help_patterns)),
                       url(r'^registration/', include(registration_patterns)))