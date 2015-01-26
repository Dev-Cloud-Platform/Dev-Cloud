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

import logging

from django.conf import settings
from django.contrib.messages import success
from django.http import HttpResponseRedirect
from django.utils.http import urlquote

from core.utils import REDIRECT_FIELD_NAME
from messages_codes import auth_error_text


def django_view(function):
    """
        Logs any exception thrown by a view.
    """
    dev_logger = logging.getLogger('dev_logger')
    def wrapper(*args, **kwargs):
        """
            Returned decorated function.
        """
        try:
            ret = function(*args, **kwargs)
        except Exception, ex:
            dev_logger.exception('General exception: %s' % str(ex))
            raise ex
        return ret

    wrapper.__module__ = function.__module__
    wrapper.__name__ = function.__name__
    wrapper.__doc__ = function.__doc__
    return wrapper

login_url = settings.LOGIN_URL



def user_permission(view_func):
    """
        \b Decorator for views with logged user permissions.
    """
    def wrap(request, *args, **kwds):
        """
            Returned decorated function.
        """
        if 'user' in request.session:
            return view_func(request, *args, **kwds)
        if request.is_ajax():
            return success(unicode(auth_error_text), status=8002)
        path = urlquote(request.get_full_path())
        tup = login_url, REDIRECT_FIELD_NAME, path
        return HttpResponseRedirect('%s?%s=%s' % tup)
    return wrap