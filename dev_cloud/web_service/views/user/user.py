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
from django_ajax.decorators import ajax
from core.settings import common
from core.utils import REDIRECT_FIELD_NAME
from core.utils.auth import session_key, update_session
from core.utils.decorators import django_view, lock_screen
from core.utils.decorators import user_permission
from database.models import Users, VirtualMachines, Tasks
from database.models.notifications import Notifications
from database.models.tasks import POSTS_PER_PAGE
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
    done_task = Tasks.objects.filter(is_succeeded=True).count()
    pending_task = Tasks.objects.filter(is_processing=True).count()

    return render_to_response(template_name,
                              dict({'users_amount': users_amount,
                                    'virtual_machines': virtual_machines,
                                    'done_task': done_task,
                                    'pending_task': pending_task}.items()
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


@ajax
@user_permission
def refresh_notification(request, template_name='app/notification/refresh_notification_list.html'):
    """
    Shows all not read notifications of user. Automatically refreshed.
    @param request:
    @param template_name:
    @return:
    """
    notification_list = Notifications.objects.filter(user_id=int(request.session[session_key]), is_read=False).order_by(
        '-create_time')

    return render_to_response(template_name, dict({'notification_list': notification_list}),
                              context_instance=RequestContext(request))


@ajax
@user_permission
def refresh_notification_notifier(request, template_name='app/notification/refresh_notification_notifier.html'):
    """
    Shows last five notification. Automatically refreshed.
    @param request:
    @param template_name:
    @return:
    """
    notification_list = Notifications.objects.filter(user_id=int(request.session[session_key]), is_read=False).order_by(
        '-create_time')[0:5]

    my_dict = []
    for notification in notification_list:
        if notification.category == 1 or notification.category == 2:
            notify_task_id = re.search(r'(\d+)', notification.notification_name).group(1)
            my_dict.append({'notification': notification, 'notify_task_id': notify_task_id})
        else:
            my_dict.append({'notification': notification})
    return render_to_response(template_name, dict({'new_notifications': my_dict}),
                              context_instance=RequestContext(request))


@ajax()
@user_permission
def mark_read_all(request):
    """
    Marks all notification to read.
    @param request:
    @return:
    """
    notification_list = Notifications.objects.filter(user_id=int(request.session[session_key]), is_read=False).order_by(
        '-create_time')

    for notification in notification_list:
        notification.is_read = True
        notification.save()


@ajax()
@user_permission
def mark_read_all_notifier(request):
    """
    Marks last five notifications to read.
    @param request:
    @return:
    """
    notification_list = Notifications.objects.filter(user_id=int(request.session[session_key]), is_read=False).order_by(
        '-create_time')[0:5]

    for notification in notification_list:
        notification.is_read = True
        notification.save()


@django_view
@user_permission
def tasks(request, task_id=None, template_name='app/task/tasks.html'):
    """
    Shows all tasks of user.
    @param request:
    @param task_id:
    @param template_name:
    @return:
    """
    tasks_list = Tasks.objects.filter(user_id=int(request.session[session_key])).order_by('-create_time')
    paginator = Paginator(tasks_list, POSTS_PER_PAGE)

    page = None
    scroll_to_task = None

    if task_id is not None:
        page = Tasks.objects.get_page(int(request.session[session_key]), task_id)
        scroll_to_task = task_id

    if request.GET.get('page') is not None:
        page = request.GET.get('page')
        scroll_to_task = None

    try:
        tasks_on_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        tasks_on_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        tasks_on_page = paginator.page(paginator.num_pages)

    return render_to_response(template_name, dict({'tasks': tasks_on_page, 'scroll_to_task': scroll_to_task}),
                              context_instance=RequestContext(request))


@ajax
@user_permission
def refresh_tasks(request, task_id=None, template_name='app/task/refresh_tasks_timeline.html'):
    """
    Shows all tasks of user. Automatically refreshed.
    @param request:
    @param task_id:
    @param template_name:
    @return:
    """
    tasks_list = Tasks.objects.filter(user_id=int(request.session[session_key])).order_by('-create_time')
    paginator = Paginator(tasks_list, POSTS_PER_PAGE)

    page = None
    scroll_to_task = 0

    if task_id is not None:
        page = Tasks.objects.get_page(int(request.session[session_key]), task_id)
        scroll_to_task = task_id

    if request.GET.get('page') is not None:
        page = request.GET.get('page')
        scroll_to_task = 0

    try:
        tasks_on_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        tasks_on_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        tasks_on_page = paginator.page(paginator.num_pages)

    return render_to_response(template_name, dict({'tasks': tasks_on_page, 'scroll_to_task': scroll_to_task}),
                              context_instance=RequestContext(request))


@ajax
@user_permission
def refresh_tasks_notifier(request, template_name='app/task/refresh_tasks_notifier.html'):
    """
    Shows pending task. Automatically refreshed.
    @param request:
    @param template_name:
    @return:
    """
    tasks_list = Tasks.objects.filter(user_id=int(request.session[session_key]), is_processing=True).order_by(
        '-create_time')
    return render_to_response(template_name, dict({'pending_tasks': tasks_list}),
                              context_instance=RequestContext(request))


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
