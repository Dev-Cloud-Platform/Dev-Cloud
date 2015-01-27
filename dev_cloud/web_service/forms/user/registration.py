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

from core.settings import common
from core.utils.recaptcha import ReCaptchaField
from core.utils.regexp import regexp_text, regexp
from database.models import Users
from web_service.forms.user.password import PasswordForm, attrs_dict


class RegistrationForm(PasswordForm):
    """
    Form for <b>registering a new user account</b>.

    Validates that the requested username is not already in use, and
    requires the password to be entered twice to catch typos.
    """
    login = forms.RegexField(regex=regexp['login'],
                             max_length=45,
                             widget=forms.TextInput(attrs=attrs_dict),
                             label=_('Username'),
                             error_messages={'invalid': regexp_text['login']})

    first = forms.CharField(max_length=45,
                            widget=forms.TextInput(attrs=attrs_dict),
                            label=_('First name'))

    last = forms.CharField(max_length=45,
                           widget=forms.TextInput(attrs=attrs_dict),
                           label=_('Last name'))

    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict, maxlength=255)),
                             label=_('Email address'))

    class Meta:
        model = Users
        fields = ('login', 'first', 'last', 'email', 'new_password', 'password2')


    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = ['login', 'first', 'last', 'email', 'new_password', 'password2']

        if common.CAPTCHA:
            self.fields['recaptcha'] = ReCaptchaField()

    def clean_login(self):
        """
        Validate that the login is alphanumeric and is not already in use.
        @return:
        """
        login = self.cleaned_data['login']

        try:
            Users._default_manager.get(login=login)
        except Users.DoesNotExist:
            return login
        raise forms.ValidationError(_("A user with that login already exists."))

    def clean_email(self):
        """
        Validate that the supplied email address is unique for the site.
        @return:
        """
        email = self.cleaned_data["email"]

        try:
            Users._default_manager.get(email=email)
        except Users.DoesNotExist:
            return email
        raise forms.ValidationError(_("This email address is already in use. Please supply a different email address."))

    def save(self, commit=True):
        """
        Modify save() method so that we can set user.is_active to False when we first create our user
        @param commit:
        @return:
        """
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.is_active = False # not active until he opens activation link
            user.save()

        return user


