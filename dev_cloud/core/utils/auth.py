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
from datetime import datetime
import cPickle
from django.core import serializers
import pickle

from core.common.states import user_active_states
from core.utils.exception import DevCloudException
from database.models.users import Users


session_key = '_auth_user_id'


def login(request, user):
    """
    Saves \c user in session.
    @param request:
    @param user:
    @return:
    """
    if session_key in request.session:
        if request.session[session_key] != user.id:
            # To avoid reusing another user's session, create a new, empty
            # session if the existing session corresponds to a different
            # authenticated user.
            request.session.flush()
    else:
        request.session.cycle_key()

    request.session[session_key] = user.id
    request.session['user'] = user.dict


def logout(session):
    """
    Removes data connected with user from the session.
    @param session:
    @return:
    """
    session.flush()


def authenticate(username, password):
    """
    Method for authentication. When successful, it returns \c user object.
    :param username:
    :param password:
    :return:
    """
    try:
        user = Users.objects.get(login=username)
    except Users.DoesNotExist:
        return None

    if user.is_active == user_active_states['ok']:
        try:
            user.last_activity = datetime.now()
            user.save()
        except:
            raise DevCloudException('user_edit')
    else:
        return user

    if user.password == password:
        return user
    else:
        return None


def update_session(request, user):
    """
    Updates data \c user in session.
    @param request:
    @param user:
    @return:
    """
    request.session['user'] = user.dict