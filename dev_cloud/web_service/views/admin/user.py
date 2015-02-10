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
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django_ajax.decorators import ajax
from core.utils.decorators import django_view, admin_permission
from database.models import Users
from web_service.forms.user.edit_user import EditUserForm
from web_service.views.user.user import generate_active


@django_view
@csrf_protect
@admin_permission
def user_activation(request, template_name='app/user_activation.html'):
    """
    Displays all users to edit.
    @param request:
    @param template_name:
    @return:
    """
    current_site = RequestSite(request)
    users = Users.objects.all()

    return render_to_response(template_name,
                              dict(
                                  {'users': users,
                                   'site': current_site,
                                   'site_name': current_site.name}.items()
                                  + generate_active('user_activation').items()),
                              context_instance=RequestContext(request))


@ajax
@csrf_protect
@admin_permission
@never_cache
def ajax_activation_edit(request, id, template_name='app/user_activation_modal.html', edit_form=EditUserForm):
    """
    Ajax edits user details by administrator.
    @param request:
    @param user_id:
    @return:
    """
    user = Users.objects.get(id=id)
    current_site = RequestSite(request)

    if request.method == 'POST':
        form = edit_form(request, user.dict, data=request.POST)
        if form.is_valid():
            users = Users.objects.all()
            template_name = 'app/user_activation_table.html'
            return render_to_response(template_name,
                                      dict(
                                          {'users': users,
                                           'site': current_site,
                                           'site_name': current_site.name}.items()
                                          + generate_active('user_activation').items()),
                                      context_instance=RequestContext(request))
    else:
        form = edit_form(request, user.dict)
        if request.is_ajax():
            return render_to_response(template_name, dict(
                {'form': form, 'site': current_site, 'id': id, 'is_superuser': request.session['user']['is_superuser'],
                 'site_name': current_site.name}.items()), context_instance=RequestContext(request))
