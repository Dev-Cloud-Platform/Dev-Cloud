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
from django.utils.translation import ugettext_lazy as _

from core.utils.decorators import user_permission
from core.utils.views import direct_to_template
from web_service.views.user.mail import mail_inbox, mail_compose, mail_message
from web_service.views.user.user import app_view, lock_screen, edit_account, members, tasks, refresh_tasks_notifier, \
    refresh_tasks, refresh_notification_notifier, refresh_notification, mark_read_all, mark_read_all_notifier

account_patterns = patterns('web_service.views.user.user',
                            url(r'^$', user_permission(direct_to_template),
                                {'template_name': 'app/account/info_account.html'},
                                name='account'),
                            url(r'^edit/$', user_permission(edit_account), name='edit_account'))

mail_patterns = patterns('web_service.views.user.mail',
                         url(r'^$', user_permission(mail_inbox), name='mail_box'),
                         url(r'^compose/$', user_permission(mail_compose), name='mail_compose'),
                         url(r'^message/$', user_permission(mail_message), name='mail_message'))

main_patterns = patterns('web_service.views.user.user',
                         url(r'^app/$', user_permission(app_view), name='app_main'),
                         url(r'^app/mailbox/', include(mail_patterns)),
                         url(r'^app/task/$', user_permission(tasks), name='tasks'),
                         url(r'^app/task/(?P<task_id>\w+)/$', user_permission(tasks), name='tasks'),
                         url(r'^app/utils/refresh_notification/$', user_permission(refresh_notification),
                             name='refresh_notification'),
                         url(r'^app/utils/refresh_notification_notifier/$',
                             user_permission(refresh_notification_notifier),
                             name='refresh_notification_notifier'),
                         url(r'^app/utils/mark_read_all/$', user_permission(mark_read_all), name='mark_read_all'),
                         url(r'^app/utils/mark_read_all_notifier/$', user_permission(mark_read_all_notifier),
                             name='mark_read_all_notifier'),
                         url(r'^app/utils/refresh_tasks/$', user_permission(refresh_tasks), name='refresh_tasks'),
                         url(r'^app/utils/refresh_tasks/(?P<task_id>\w+)/$', user_permission(refresh_tasks),
                             name='refresh_tasks'),
                         url(r'^app/utils/refresh_tasks_notifier/$', user_permission(refresh_tasks_notifier),
                             name='refresh_tasks_notifier'),
                         url(r'^app/members/$', user_permission(members), name='members'),
                         url(r'^lock_screen/$', lock_screen, name='lock_screen'))

urlpatterns = patterns('',
                       url(r'^account/', include(account_patterns)),
                       url(r'^main/', include(main_patterns)))
