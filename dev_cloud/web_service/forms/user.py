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
from django import forms
from django.utils.translation import ugettext_lazy as _
from dev_cloud.core.utils.regexp import regexp, regexp_text


class AuthenticationForm(forms.Form):
    """
        Class for <b>login</b> form.
    """
    username = forms.CharField(max_length=45,
                               label=_('Username'),
                               widget=forms.TextInput(attrs={'tabindex': '1', 'class': 'required'}))

    password = forms.RegexField(regex=regexp['password'],
                                max_length=32,
                                label=_('Password'),
                                widget=forms.PasswordInput(attrs={'tabindex': '2', 'class': 'required'}),
                                error_messages={'invalid': regexp_text['password']})



    def __init__(self, request=None, *args, **kwargs):
        """
            If request is passed in, the form will validate that cookies are
            enabled.
            @note
            Note that the \c request (a HttpRequest object) must have set
            a cookie with the key \c TEST_COOKIE_NAME and value \c TEST_COOKIE_VALUE
            before running this validation.
        """
        self.request = request
        self.user_cache = None
        super(AuthenticationForm, self).__init__(*args, **kwargs)



    def get_user(self):
        """
            Returns cached user object instance.
        """
        return self.user_cache