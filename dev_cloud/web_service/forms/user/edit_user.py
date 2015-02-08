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
from core.utils.auth import update_session
from core.utils.exception import DevCloudException
from database.models import Users

from registration import forms
from django.utils.translation import ugettext_lazy as _
from web_service.forms.user.password import EditPasswordForm


class EditUserForm(EditPasswordForm):
    """
    Class for <b>edit account</b> form.
    """

    first = forms.CharField(max_length=45,
                            widget=forms.TextInput(attrs={'class': 'form-control'}),
                            label=_('First name'))

    last = forms.CharField(max_length=45,
                           widget=forms.TextInput(attrs={'class': 'form-control'}),
                           label=_('Last name'))

    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'maxlength': 255}),
                             label=_('Email address'))

    class Meta:
        fields = ('first', 'last', 'email', 'new_password', 'password2')

    def __init__(self, request=None, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = ['first', 'last', 'email', 'new_password', 'password2']
        self.request = request
        self.instance = request.session['user']

        try:
            pass
            self.fields['first'].initial = self.instance['first']
            self.fields['last'].initial = self.instance['last']
            self.fields['email'].initial = self.instance['email']
        except Exception:
            pass

    def clean(self):
        """
        Update data on the related User object as well.
        @param args:
        @param kwargs:
        @return:
        """
        try:
            user = Users.objects.get(login=self.instance['login'])
        except Users.DoesNotExist:
            return None

        try:
            user.name = self.cleaned_data['first']
            user.lastname = self.cleaned_data['last']
            user.email = self.cleaned_data['email']

            if self.cleaned_data['new_password'] != '' or self.cleaned_data['new_password'] is not None:
                user.password = hashlib.sha1(self.cleaned_data['new_password']).hexdigest()
                del self.cleaned_data['new_password']
                del self.cleaned_data['password2']

            user.save()
            update_session(self.request, user)
        except:
            raise DevCloudException('user_edit')

        return self.cleaned_data
