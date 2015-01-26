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
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from core.utils.recaptcha import ReCaptchaField
from core.utils.regexp import regexp_text, regexp
from core.utils.views import make_request
from web_service.forms.user.password import PasswordForm, attrs_dict


class RegistrationForm(PasswordForm):
    """
        Form for <b>registering a new user account</b>.

        Validates that the requested username is not already in use, and
        requires the password to be entered twice to catch typos.
    """
    login = forms.RegexField(regex=regexp['login'],
                             max_length=63,
                             widget=forms.TextInput(attrs=attrs_dict),
                             label=_('Username'),
                             error_messages={'invalid': regexp_text['login']})
    first = forms.CharField(max_length=63,
                            widget=forms.TextInput(attrs=attrs_dict),
                            label=_('First name'))
    last = forms.CharField(max_length=63,
                           widget=forms.TextInput(attrs=attrs_dict),
                           label=_('Last name'))
    organization = forms.CharField(max_length=63,
                                   widget=forms.TextInput(attrs=attrs_dict),
                                   label=_('Organization'))
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict, maxlength=255)),
                             label=_('Email address'))

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        self.fields.keyOrder = ['login', 'first', 'last', 'organization', 'email', 'new_password', 'password2']

        if settings.CAPTCHA:
            self.fields['recaptcha'] = ReCaptchaField()

    def clean_login(self):
        """
            Validate that the login is alphanumeric and is not already in use.
        """
        response = make_request('guest/user/exists/', {'login': self.cleaned_data['login']})

        if response['data'] == False:
            return self.cleaned_data['login']
        else:
            raise forms.ValidationError(_("A user with that login already exists."))

    def clean_email(self):
        """
            Validate that the supplied email address is unique for the site.
        """
        response = make_request('guest/user/email_exists/', {'email': self.cleaned_data['email']})

        if response['data'] == False:
            return self.cleaned_data['email']
        else:
            raise forms.ValidationError(
                _("This email address is already in use. Please supply a different email address."))