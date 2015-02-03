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

import re

from django.contrib.sites.models import RequestSite
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from core.common.states import registration_states
from core.settings import common
from core.utils import REDIRECT_FIELD_NAME
from core.utils.auth import session_key
from core.utils.decorators import django_view
from core.utils.registration.mail import send_contact_message
from core.utils.registration.registration import register, activate
from database.models import Users
from web_service.forms.user.authenticate import AuthenticationForm
from web_service.forms.user.contact import ContactForm
from web_service.forms.user.registration import RegistrationForm


@django_view
@csrf_protect
@never_cache
def login(request, template_name='auth/login.html', redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm):
    """
    Login page handling.
    @param request:
    @param template_name:
    @param redirect_field_name:
    @param authentication_form:
    @return:
    """
    redirect_to = request.REQUEST.get(redirect_field_name, '')
    if request.method == 'POST':
        form = authentication_form(data=request.POST)
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
                              {'form': form,
                               redirect_field_name: redirect_to,
                               'site': current_site,
                               'site_name': current_site.name,
                               }, context_instance=RequestContext(request))


@django_view
def logout(request, next_page=None, template_name='auth/logged_out.html', redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Logout and redirection to the right next page (\c next_page).
    @param request:
    @param next_page:
    @param template_name:
    @param redirect_field_name:
    @return:
    """
    from core.utils.auth import logout as auth_logout
    auth_logout(request.session)

    if next_page is None:
        redirect_to = request.REQUEST.get(redirect_field_name, '')
        if redirect_to:
            return HttpResponseRedirect(redirect_to)
        else:
            return render_to_response(template_name, {'title': _('Logged out')}, context_instance=RequestContext(request))
    else:
        # Redirect to this page until the session has been cleared.
        return HttpResponseRedirect(next_page or request.path)


@django_view
def change_language(request, lang, success_url='app_main'):
    """
    View changing page language.
    @param request:
    @param lang:
    @param success_url:mai
    @return:
    """
    request.session['django_language'] = lang
    request.session['_language'] = lang
    request.session.modified = True

    return redirect(request.META['HTTP_REFERER'] or success_url)


@django_view
def reg_register(request, form_class=RegistrationForm, template_name='registration/registration_form.html'):
    """
    Registration form's handling.
    @param request:
    @param form_class:
    @param template_name:
    @return:
    """
    if request.method == 'POST':
        form = form_class(data=request.POST)
        if form.is_valid():
            response = register(**form.cleaned_data)

            if response['registration_state'] == registration_states['completed']:
                return redirect('registration_completed')

            elif response['registration_state'] == registration_states['mail_confirmation']:
                return redirect('registration_mail_confirmation')

            elif response['registration_state'] == registration_states['admin_confirmation']:
                return redirect('registration_admin_confirmation')

            else:
                import logging
                dev_logger = logging.getLogger('dev_logger')
                dev_logger.error('Registration error: %s' % response['status'])
                dev_logger.error(response['data'])
                return redirect('registration_error')
    else:
        form = form_class()

    return render_to_response(template_name, {'form': form}, RequestContext(request))


@django_view
def reg_activate(request, **kwargs):
    """
    User's email address's confirmation (by entering the HTTP address provided in email message).
    @param request:
    @param kwargs:
    @return:
    """
    act_response = activate(**kwargs)
    if act_response:
        if act_response['registration_state'] == registration_states['completed']:
            return redirect('activation_completed')

        if act_response['registration_state'] == registration_states['admin_confirmation']:
            return redirect('activation_admin_confirmation')

    return redirect('activation_error')

@django_view
def contact(request, form_class=ContactForm, template_name='main/contact.html'):
    """
    View handling help form.
    @param request:
    @param form_class:
    @param template_name:
    @return:
    """
    if request.method == 'POST':
        form = form_class(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']
            message = form.cleaned_data['message']
            subject = _('From user:') + name + ', email: ' + email
            send_contact_message(subject, message)

            return redirect('contact')
    else:
        form = form_class()

    return render_to_response(template_name, dict({'form': form}.items()),
                              context_instance=RequestContext(request))