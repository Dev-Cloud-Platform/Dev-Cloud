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
from web_service.forms.user.password import attrs_dict


class ContactForm(forms.Form):
    """
    Class for <b>send mail</b> form.
    """
    name = forms.CharField(max_length=45,
                           label=_('Name'),
                           widget=forms.TextInput(attrs={'tabindex': '1', 'class': 'required'}))

    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict, tabindex=2, maxlength=255)),
                             label=_('Email'))

    message = forms.CharField(min_length=1,
                              label=_('Message'),
                              widget=forms.Textarea(
                                  attrs=dict(attrs_dict, cols=12, rows=6, tabindex=3)))

    class Meta:
        fields = ('name', 'email', 'message')

    def __init__(self, request=None, *args, **kwargs):
        """
        Initial method.
        @param request:
        @param args:
        @param kwargs:
        @return:
        """
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = ['name', 'email', 'message']