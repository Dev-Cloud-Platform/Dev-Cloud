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
from django.contrib.sites.models import RequestSite
from django.shortcuts import render_to_response
from django.template import RequestContext
from core.utils.decorators import django_view, user_permission
from web_service.views.user.user import generate_active


@django_view
@user_permission
def mail_inbox(request, template_name='app/mail/mailbox.html'):
    """
    TODO
    @param request:
    @param template_name:
    @return:
    """
    current_site = RequestSite(request)
    return render_to_response(template_name,
                              dict({'site': current_site,
                                    'site_name': current_site.name}.items()
                                   + generate_active('mail_box_inbox').items()),
                              context_instance=RequestContext(request))


@django_view
@user_permission
def mail_compose(request, template_name='app/mail/compose.html'):
    """
    TODO
    @param request:
    @param template_name:
    @return:
    """
    current_site = RequestSite(request)
    return render_to_response(template_name,
                              dict({'site': current_site,
                                    'site_name': current_site.name}.items()
                                   + generate_active('mail_box_compose').items()),
                              context_instance=RequestContext(request))


@django_view
@user_permission
def mail_message(request, template_name='app/mail/message.html'):
    """
    TODO
    @param request:
    @param template_name:
    @return:
    """
    current_site = RequestSite(request)
    return render_to_response(template_name, dict({'site': current_site, 'site_name': current_site.name}.items()),
                              context_instance=RequestContext(request))