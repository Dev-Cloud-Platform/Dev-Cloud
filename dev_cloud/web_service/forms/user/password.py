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
        """
        if 'new_password' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['new_password'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields didn't match."))

            self.cleaned_data['new_password'] = hashlib.sha1(self.cleaned_data['new_password']).hexdigest()
            del self.cleaned_data['password2']
        return self.cleaned_data
