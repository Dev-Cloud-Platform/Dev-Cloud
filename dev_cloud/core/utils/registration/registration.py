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

import random
import re
from smtplib import SMTPRecipientsRefused
import string
import datetime

from django.shortcuts import get_object_or_404
from django.utils import timezone

from django.db import DatabaseError
from django.utils.translation import ugettext as _

from core.settings import config
from core.common.states import user_active_states, registration_states, notification_category
from core.settings import common
from core.utils.exception import DevCloudException
from core.utils.registration import mail
from database.models import Users, Notifications
from core.utils.log import error

SHA1_RE = re.compile('^[A-Z0-9]{40}$')


def registration(first, last, login, email, new_password, dev_cloud_data):
    """
    Registers new user.
    @param first: firstname to set
    @param last: lastname to set
    @param login: login to set
    @param email: email to set
    @param new_password: password to set
    @param dev_cloud_data: additional data
    @return:
    """

    user = Users()
    user.name = first
    user.lastname = last
    user.login = login
    user.email = email
    user.password = new_password
    user.create_time = user.last_activity = timezone.now()
    user.is_active = user_active_states['inactive']
    user.activation_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for n in range(40))

    try:
        user.save()
    except:
        raise DevCloudException('user_register')

    reg_state = -1
    if common.MAILER_ACTIVE:
        try:
            # mail the user
            mail.send_activation_email(user.activation_key, user, dev_cloud_data)
        except SMTPRecipientsRefused:
            reg_state = registration_states['error']
        reg_state = registration_states['mail_confirmation']
    elif common.REGISTRATION_CLOSED:
        reg_state = registration_states['disallowed']
    else:
        if common.AUTOACTIVATION:

            user.is_active = user_active_states['ok']
            user.activation_date = timezone.now()
            user.act_key = ''

            reg_state = registration_states['completed']
        else:
            user.is_active = user_active_states['email_confirmed']

            reg_state = registration_states['admin_confirmation']

        try:
            user.save()
        except:
            raise DevCloudException('user_activate')

    return {'user': user.dict, 'registration_state': reg_state}


def register(**kwargs):
    """
    Method turns keyword arguments (which describe user) into a dictionary and registers the user
    @param kwargs:
    @return:
    """
    if 'recaptcha' in kwargs:
        kwargs.pop('recaptcha')
    kwargs['dev_cloud_data'] = config.DEV_CLOUD_DATA

    return registration(**kwargs)


def activate(activation_key):
    """
    Method checks, if \c activation_key is ok. If so, it activates user.
    @param activation_key:
    @return:
    """
    if SHA1_RE.search(activation_key):
        user = get_object_or_404(Users, activation_key=activation_key)
        user.is_active = user_active_states['email_confirmed']
        reg_state = registration_states['admin_confirmation']

        if common.AUTOACTIVATION:
            user.is_active = user_active_states['ok']
            reg_state = registration_states['completed']

        user.last_activity = timezone.now()
        user.act_key = ''

        try:
            user.save()
        except:
            raise DevCloudException('user_activate')

        if common.MAILER_ACTIVE and reg_state == registration_states['admin_confirmation']:
            try:
                mail.send_admin_registration_notification(user.dict, config.DEV_CLOUD_DATA)
                notify_all_superusers(user)
            except SMTPRecipientsRefused:
                pass

        return {'user': user.dict, 'registration_state': reg_state}

    return False


def notify_all_superusers(user):
    """
    Notify all super user about new registered user.
    @param user: registered user.
    """
    if user:
        try:
            superusers = Users.objects.filter(is_superuser=True)
            for superuser in superusers:
                Notifications.objects.create(
                    notification_name="New user " + user.login + " registered",
                    notification_information="Registered as" + user.name + " " + user.lastname,
                    category=notification_category['registered_new_user'],
                    is_read=False,
                    create_time=datetime.datetime.now(),
                    user_id=superuser.id
                )
        except DatabaseError:
            error(user.id, _("DataBase - Problem with create a notifications"))
