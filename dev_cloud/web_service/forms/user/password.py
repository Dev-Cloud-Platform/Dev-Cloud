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
from database.models import Users

from core.utils.regexp import regexp, regexp_text


attrs_dict = {'class': 'required'}


class PasswordForm(forms.Form):
    """
     Class for <b>setting password</b> form.
    """
    new_password = forms.RegexField(regex=regexp['password'],
                                    max_length=32,
                                    widget=forms.PasswordInput(attrs=dict(attrs_dict)),
                                    label=_("Password"),
                                    error_messages={'invalid': regexp_text['password']})

    password2 = forms.RegexField(regex=regexp['password'],
                                 max_length=32,
                                 widget=forms.PasswordInput(attrs=dict(attrs_dict)),
                                 label=_("Password confirmation"),
                                 error_messages={'invalid': regexp_text['password']})

    def clean(self):
        """
        Checks if given passwords match.
        @return:
        """

        if 'new_password' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['new_password'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields didn't match."))

            self.cleaned_data['new_password'] = hashlib.sha1(self.cleaned_data['new_password']).hexdigest()
            del self.cleaned_data['password2']
        return self.cleaned_data


class PasswordResetForm(forms.Form):
    """
        Class of the <b>password's reset</b> form.
        """
    email = forms.EmailField(label=_("E-mail"),
                             max_length=255)

    @staticmethod
    def email_exists(email):
        """
            Method checks, whether user with specified @prm{email} already exists.
            @parameter{email,string}
            @response{bool) True if @prm{email} is registered
            @response{bool) False if @prm{email} isn't registered
            """
        return Users.objects.filter(email__exact=email).exists()

    def clean_email(self):
        """
            Validates that a user exists with the given e-mail address.
            @return:
            """
        email = self.cleaned_data['email']

        if self.email_exists(email):
            return email
        raise forms.ValidationError(_('Incorrect email address.'))


class SetPasswordForm(forms.Form):
    """
    Class of the <b>password edition (doesnt's require giving the previous one)</b> form.
    """
    new_password1 = forms.RegexField(regex=regexp['password'],
                                     max_length=255,
                                     widget=forms.PasswordInput(attrs=dict(attrs_dict)),
                                     label=_("New password"),
                                     error_messages={'invalid': regexp_text['password']})

    new_password2 = forms.RegexField(regex=regexp['password'],
                                     max_length=255,
                                     widget=forms.PasswordInput(attrs=dict(attrs_dict)),
                                     label=_("New password confirmation"),
                                     error_messages={'invalid': regexp_text['password']})

    def clean(self):
        """
         Validates that a password are the same.
        @return:
        """
        if 'new_password1' in self.cleaned_data and 'new_password2' in self.cleaned_data:
            if self.cleaned_data['new_password1'] != self.cleaned_data['new_password2']:
                raise forms.ValidationError(_("The two password fields didn't match."))

            self.cleaned_data['new_password1'] = hashlib.sha1(self.cleaned_data['new_password1']).hexdigest()
            del self.cleaned_data['new_password2']

        return self.cleaned_data


class EditPasswordForm(forms.Form):
    """
     Class for <b>setting password</b> form.
    """
    new_password = forms.RegexField(regex=regexp['password'],
                                    max_length=32,
                                    required=False,
                                    widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                    label=_("Password"))

    password2 = forms.RegexField(regex=regexp['password'],
                                 max_length=32,
                                 required=False,
                                 widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                 label=_("Password confirmation"))

    def clean(self):
        """
        Checks if given passwords match.
        @return:
        """

        if 'new_password' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['new_password'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields didn't match."))

            self.cleaned_data['new_password'] = hashlib.sha1(self.cleaned_data['new_password']).hexdigest()
            del self.cleaned_data['password2']
        return self.cleaned_data