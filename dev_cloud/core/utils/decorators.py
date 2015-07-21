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
import datetime

from django.contrib.messages import success
from django.db import transaction
from django.http import HttpResponseRedirect
from django.http.response import Http404
from django.utils.http import urlquote

from core.settings import common
from core.utils import REDIRECT_FIELD_NAME
from core.utils.auth import session_key
from database.models import Users, Tasks
from messages_codes import auth_error_text

from core.utils.log import error
from django.utils.translation import ugettext as _


@transaction.atomic
def check_status(view_func):
    """
    Check status is called by actor decorators defined in core.utils.decorators:
    - core.utils.decorators.django_view

    It calls decorated functions, additionally performing several tasks.

    @return: HttpResponse response with content of JSON-ed tuple
    (status, data), where status should be "ok" if everything went fine.
    """

    def wrap(request, *args, **kwds):
        """
        Returned decorated function.
        @param request:
        @param args:
        @param kwds:
        @return:
        """
        resp = {'test': 'test2'}

        try:
            processing_tasks = Tasks.objects.filter(user_id=int(request.session[session_key]),
                                                    is_processing=True).order_by('-create_time')
        except:
            processing_tasks = None

        request.session['resp'] = resp

        # TODO: Add data about notifications and tasks.

        return view_func(request, *args, **kwds)

    return wrap


@transaction.atomic
def django_view(function):
    """
    Logs any exception thrown by a view.
    @param function:
    @return:
    """
    dev_logger = logging.getLogger('dev_logger')

    @check_status
    def wrapper(*args, **kwargs):
        """
        Returned decorated function.
        @param args:
        @param kwargs:
        @return:
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


login_url = common.LOGIN_URL


@transaction.atomic
def user_permission(view_func):
    """
    \b Decorator for views with logged user permissions.
    @param view_func:
    @return:
    """

    def wrap(request, *args, **kwds):
        """
        Returned decorated function.
        @param request:
        @param args:
        @param kwds:
        @return:
        """
        try:
            user = Users.objects.get(id=int(request.session[session_key]))
        except:
            user = None

        if user:
            return view_func(request, *args, **kwds)

        if request.is_ajax():
            return success(unicode(auth_error_text), status=8002)

        path = urlquote(request.get_full_path())
        tup = login_url, REDIRECT_FIELD_NAME, path
        return HttpResponseRedirect('%s?%s=%s' % tup)

    return wrap


@transaction.atomic
def admin_permission(view_func):
    """
    \b Decorator for views with logged admin permissions.
    @param view_func:
    @return:
    """

    @user_permission
    def wrap(request, *args, **kwds):
        """
        Returned decorated function.
        @param request:
        @param args:
        @param kwds:
        @return:
        """

        if request.session['user']['is_superuser']:
            return view_func(request, *args, **kwds)

        raise Http404('Access denied')

    return wrap


@transaction.atomic
def load_basic_data(method_to_decorate):
    """
    \b Decorator for views with with decorate with additional information.
    @param function:
    @return:
    """

    def wrap(request, *args, **kwds):
        """
        Returned decorated function.
        @param request:
        @param args:
        @param kwds:
        @return:
        """
        try:
            user = Users.objects.get(id=int(request.session[session_key]))
            request.session['name'] = user.name + ' ' + user.lastname
        except:
            user = None

        if user:
            return method_to_decorate(request, *args, **kwds)

    return wrap


def lock_screen(view_func):
    """
    \b Decorator for views with logged user permissions.
    @param view_func:
    @return:
    """

    def wrap(request, *args, **kwds):
        """
        Returned decorated function.
        @param request:
        @param args:
        @param kwds:
        @return:
        """
        try:
            if request.session['user'] is not None:
                return view_func(request, *args, **kwds)
        except:
            pass

        path = urlquote(request.get_full_path())
        tup = login_url, REDIRECT_FIELD_NAME, path
        return HttpResponseRedirect('%s?%s=%s' % tup)

    return wrap


def manual_transaction(function):
    """
    Decorator to create safe transactions.
    Behaviour similar to transaction.atomic.

    A.D. Atomic
        Atomic blocks can be nested. In this case, when an inner block completes successfully, its effects can still be
        rolled back if an exception is raised in the outer block at a later point.
    """

    def wrap(*args, **kwargs):
        transaction.set_autocommit(False)
        try:
            ret = function(*args, **kwargs)
        except:
            transaction.rollback()
            error(None, _("DataBase - manual_transaction call rollback"))
            raise
        else:
            transaction.commit()
        finally:
            transaction.set_autocommit(True)

        return ret

    return wrap


class dev_cloud_task(object):
    """
    Decorator to automatically register task into database.
    """

    def __init__(self, arg1):
        """
        If there are decorator arguments, the function
        to be decorated is not passed to the constructor!
        """
        self.task_name = arg1
        self.task = None

    @manual_transaction
    def __call__(self, function):
        """
        If there are decorator arguments, __call__() is only called
        once, as part of the decoration process! You can only give
        it a single argument, which is the function object.
        """

        def wrapped_function(*args):
            try:
                self.task = Tasks.objects.create(task_name=self.task_name, is_processing=True,
                                                 create_time=datetime.datetime.now(), user_id=args[0])
            except Exception:
                error(None, _("DataBase - Problem with create new task"))

            ret = function(*args)

            if self.task:
                try:
                    self.task.is_processing = False
                    self.task.save()
                except Exception:
                    error(None, _("DataBase - Problem with update a task"))

            return ret

        return wrapped_function


