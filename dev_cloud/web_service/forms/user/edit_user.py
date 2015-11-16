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

from core.utils.exception import DevCloudException
from database.models import Users

from registration import forms
from django.utils.translation import ugettext_lazy as _
from web_service.forms.user.password import EditPasswordForm


class EditUserForm(EditPasswordForm):
    """
    Class for <b>edit account</b> form.
    """
    CHOICES = [
        ('0', _('Inactive')),
        ('1', _('Email confirmed')),
        ('2', _('Ok')),
        ('3', _('Blocked'))
    ]

    first = forms.CharField(max_length=45,
                            widget=forms.TextInput(attrs={'class': 'form-control'}),
                            label=_('First name'))

    last = forms.CharField(max_length=45,
                           widget=forms.TextInput(attrs={'class': 'form-control'}),
                           label=_('Last name'))

    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'maxlength': 255}),
                             label=_('Email address'))

    image = forms.ImageField(label=_('Select image'),
                             required=False)

    active = forms.ChoiceField(label=_('Activation status'), choices=CHOICES, required=False,
                               widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        fields = ('first', 'last', 'email', 'image', 'active', 'new_password', 'password2')

    def __init__(self, request, instance, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = ['first', 'last', 'email', 'image', 'active', 'new_password', 'password2']
        self.instance = instance
        self.request = request

        try:
            self.fields['first'].initial = self.instance['first']
            self.fields['last'].initial = self.instance['last']
            self.fields['email'].initial = self.instance['email']
            self.fields['active'].initial = self.instance['is_active']
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

            if len(self.cleaned_data['active']):
                user.is_active = self.cleaned_data['active']

            if self.request.FILES.get('image', None) is not None:
                user.save_picture(user, self.request)

            if len(self.cleaned_data['new_password']):
                user.password = hashlib.sha1(self.cleaned_data['new_password']).hexdigest()
                del self.cleaned_data['new_password']
                del self.cleaned_data['password2']

            user.save()
        except Exception as e:
            raise DevCloudException('user_edit ' + str(e))

        return self.cleaned_data
