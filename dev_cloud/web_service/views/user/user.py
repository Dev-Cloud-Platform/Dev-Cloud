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
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

import re
from core.settings import common
from core.utils import REDIRECT_FIELD_NAME
from core.utils.auth import session_key, update_session
from core.utils.decorators import django_view, lock_screen
from core.utils.decorators import user_permission
from database.models import Users, VirtualMachines, Tasks
from web_service.forms.user.edit_user import EditUserForm
from web_service.forms.user.unlock import UnlockForm


def generate_active(selected_item):
    """
    Returns dict for selected item.
    @param selected_item: Selected item to display.
    @return: Dict with selected item.
    """
    dict = {'dashboard': '',
            'create_env_own': '',
            'create_env_pre': '',
            'manage_env': '',
            'mail_box_inbox': '',
            'mail_box_compose': '',
            'mail_box_view': '',
            'user_activation': '',
            'members': '',
            'lock_screen': ''}

    if selected_item is not None:
        dict[selected_item] = 'active'

    return dict


@django_view
@user_permission
def app_view(request, template_name='app/main.html'):
    """
    View handling main app.
    @param request:
    @param template_name:
    @return:
    """
    users_amount = Users.objects.count()
    virtual_machines = VirtualMachines.objects.count()

    return render_to_response(template_name,
                              dict({'users_amount': users_amount,
                                    'virtual_machines': virtual_machines}.items()
                                   + generate_active('dashboard').items()),
                              context_instance=RequestContext(request))


@django_view
@user_permission
def members(request, template_name='app/members.html'):
    """
    Shows all members.
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
                                  + generate_active('members').items()),
                              context_instance=RequestContext(request))


@django_view
@user_permission
def tasks(request, template_name='app/tasks.html'):
    """
    Shows all tasks of user.
    @param request:
    @param template_name:
    @return:
    """
    tasks_list = Tasks.objects.filter(user_id=int(request.session[session_key])).order_by('-create_time')
    paginator = Paginator(tasks_list, 25)  # Show 25 contacts per page

    page = request.GET.get('page')

    try:
        tasks = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        tasks = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        tasks = paginator.page(paginator.num_pages)

    return render_to_response(template_name, dict({'tasks': tasks}), context_instance=RequestContext(request))


@django_view
@csrf_protect
@never_cache
@lock_screen
def lock_screen(request, template_name='app/lock_screen.html', redirect_field_name=REDIRECT_FIELD_NAME,
                authentication_form=UnlockForm):
    """
    Log out removes auth id but left name and other stuff.
    @param request:
    @param template_name:
    @return:
    """
    redirect_to = request.REQUEST.get(redirect_field_name, '')
    if request.method == 'POST':
        form = authentication_form(request, data=request.POST)
        if form.is_valid():
            from core.utils.auth import login as auth_login
            # Light security check -- make sure redirect_to isn't garbage.
            if not redirect_to or ' ' in redirect_to:
                redirect_to = common.LOGIN_REDIRECT_URL

            # Heavier security check -- redirects to http://example.com should
            # not be allowed, but things like /view/?param=http://example.com
            # should be allowed. This regex checks if there is a '//' *before*
            # a question mark.
            elif '//' in redirect_to and re.match(r'[^\?]*//', redirect_to):
                redirect_to = common.LOGIN_REDIRECT_URL

            # Okay, security checks complete. Log the user in.
            user = form.get_user()
            user.set_password(form.cleaned_data['password'])
            auth_login(request, user)

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

            return HttpResponseRedirect(redirect_to)
    else:
        request.session[session_key] = session_key
        form = authentication_form(request)

    try:
        user = Users.objects.get(id=int(request.session[session_key]))
    except:
        user = None

    if user:
        return HttpResponseRedirect(reverse('app_main'))

    request.session.set_test_cookie()
    current_site = RequestSite(request)

    return render_to_response(template_name,
                              dict(
                                  {'form': form,
                                   redirect_field_name: redirect_to,
                                   'site': current_site,
                                   'site_name': current_site.name}.items()
                                  + generate_active('lock_screen').items()),
                              context_instance=RequestContext(request))


@django_view
@csrf_protect
@never_cache
@user_permission
def edit_account(request, template_name='app/account/edit_account.html', edit_form=EditUserForm):
    """
    Edits the user data such as name, e-mail or password.
    @param request:
    @param template_name:
    @param edit_form:
    @return:
    """
    instance = request.session.get('user', None)

    if instance is None:
        raise Http404('a was not found')

    if request.method == 'POST':
        form = edit_form(request, request.session['user'], data=request.POST)
        if form.is_valid():
            user = Users.objects.get(login=request.session['user']['login'])
            update_session(request, user)
    else:
        form = edit_form(request, request.session['user'])

    current_site = RequestSite(request)

    return render_to_response(template_name, dict({'form': form, 'site': current_site,
                                                   'site_name': current_site.name}.items()),
                              context_instance=RequestContext(request))