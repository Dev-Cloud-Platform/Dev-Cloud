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

import hashlib

from django import forms
from django.utils.translation import ugettext_lazy as _

from core.common.states import user_active_states
from core.utils.auth import authenticate
from core.utils.regexp import regexp, regexp_text


class UnlockForm(forms.Form):
    """
    Class for <b>unlock</b> form.
    """

    password = forms.RegexField(regex=regexp['password'],
                                max_length=32,
                                label=_('Password'),
                                widget=forms.PasswordInput(
                                    attrs={'tabindex': '1', 'class': 'form-control', 'placeholder': 'Password'}),
                                error_messages={'invalid': regexp_text['password']})

    def __init__(self, request=None, *args, **kwargs):
        """
        If request is passed in, the form will validate that cookies are
        enabled.
        @note
        Note that the \c request (a HttpRequest object) must have set
        a cookie with the key \c TEST_COOKIE_NAME and value \c TEST_COOKIE_VALUE
        before running this validation.
        @param request:
        @param args:
        @param kwargs:
        @return:
        """
        self.request = request
        self.user_cache = None
        super(UnlockForm, self).__init__(*args, **kwargs)

    def get_user(self):
        """
        Returns cached user object instance.
        @return:
        """
        return self.user_cache

    def clean(self):
        """
        Validates the password.
        :return:
        """
        if not self.cleaned_data.get('password'):
            return None
        self.cleaned_data['password'] = hashlib.sha1(self.cleaned_data['password']).hexdigest()

        username = self.request.session['user']['login']
        password = self.cleaned_data['password']

        self.user_cache = authenticate(username, password)

        if self.user_cache is None:
            raise forms.ValidationError(
                _("Please enter a correct password. Note that field is case-sensitive."))
        elif self.user_cache.is_active == user_active_states['inactive']:
            raise forms.ValidationError(_(
                "Account has not been activated yet. Please, click on the activation link in the email sent to you after the registration step."))
        elif self.user_cache.is_active == user_active_states['email_confirmed']:
            raise forms.ValidationError(
                _("This account is inactive. Please wait for system operator to activate your account."))

        if self.request:
            if not self.request.session.test_cookie_worked():
                raise forms.ValidationError(
                    _("Your Web browser doesn't appear to have cookies enabled. Cookies are required for logging in."))

        return self.cleaned_data
