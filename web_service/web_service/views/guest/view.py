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

import datetime

def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>Teraz jest %s.</body></html>" % now
    return HttpResponse(html)

def hello(request):
    return HttpResponse("Hello World!")

def hours_ahead(request, offset):
        offset = int(offset)
        dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
        html = "<html><body>Za %s godzin(y) będzię %s.</body></html>" % (offset, dt)
        return  HttpResponse(html)