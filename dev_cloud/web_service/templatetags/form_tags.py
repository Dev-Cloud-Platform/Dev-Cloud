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
from django import template


register = template.Library()


@register.inclusion_tag('tags/fieldsetForm.html')
def show_fieldsetform(form):
    """
    Renders given form without marking required fields.
    @param form:
    @return:
    """
    return {'form': form, 'required_fields': True}


@register.inclusion_tag('tags/fieldsetForm.html')
def show_fieldsetform_nrf(form):
    """
    Renders given form with required fields marked.
    @param form:
    @return:
    """
    return {'form': form, 'required_fields': False}


@register.inclusion_tag('tags/sendForm.html')
def show_sendform(form):
    """
    Renders given form without marking required fields.
    @param form:
    @return:
    """
    return {'form': form, 'required_fields': True}


@register.inclusion_tag('tags/loginForm.html')
def show_loginform(form):
    """
    Renders given form without marking required fields.
    @param form:
    @return:
    """
    return {'form': form, 'required_fields': True}


@register.inclusion_tag('tags/accountForm.html')
def show_accountform(form, is_superuser):
    """
    Renders given form without marking required fields.
    @param form:
    @return:
    """
    return {'form': form, 'required_fields': False, 'is_superuser': is_superuser}
