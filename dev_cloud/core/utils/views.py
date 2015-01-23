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
from dev_cloud.core.utils import check_response_errors
from dev_cloud.core.utils.decorators import django_view


@django_view
def direct_to_template(request, template_name, content_type=None):
    """
        Returns rendered template as HttpResponse.
    """
    context = RequestContext(request)
    template = loader.get_template(template_name)
    return HttpResponse(template.render(context), content_type=content_type)



def make_request(url, data, user=None):
    """
        Adds authorization-related information to data dictionary and makes a request to CLM
        using given url and data dictionary.
    """
    if not url.startswith('guest'):
        data.update({'login': user.username, 'password': user.password, 'cm_id': user.cm_id})
    if url.startswith('admin_cm'):
        data.update({'cm_password': user.cm_password})

    return None #CLM.send_request(url, False if url in not_to_be_logged_urls else True, **data) #WTF ??



def prep_data(request_urls, session):
    """
        Returns a dictionary with results of REST request.
    """
    data = None
    user = session.get('user')
    if request_urls is not None:
        data = {}
        # function_both is dictionary with pairs: key -> url
        if isinstance(request_urls, dict):
            for (key, val) in request_urls.iteritems():
                url = val
                args = {}
                if isinstance(val, tuple):
                    url = val[0]
                args = val[1]
            data[key] = check_response_errors(make_request(url, args, user=user), session)['data']
        # a simple string without any params
        elif isinstance(request_urls, str):
            data = check_response_errors(make_request(request_urls, {}, user=user), session)['data']
        # a simple string with params as a tuple
        elif isinstance(request_urls, tuple):
            data = check_response_errors(make_request(request_urls[0], request_urls[1], user=user), session)['data']

    return data