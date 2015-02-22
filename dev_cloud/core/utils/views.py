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
from django.http import HttpResponse
from django.template import RequestContext, loader

from decorators import django_view


@django_view
def direct_to_template(request, template_name, content_type=None):
    """
    Returns rendered template as HttpResponse.
    @param request:
    @param template_name:
    @param content_type:
    @return:
    """
    context = RequestContext(request)
    template = loader.get_template(template_name)
    return HttpResponse(template.render(context), content_type=content_type)




