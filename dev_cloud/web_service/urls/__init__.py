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
from django.conf import settings
from django.conf.urls import patterns, url, include
from django.contrib import admin as admin_page

from core.utils.views import direct_to_template
from web_service.views.errors.error_404 import bad_request
from web_service.views.errors.error_500 import server_error


admin_page.autodiscover() # See: https://docs.djangoproject.com/en/dev/ref/contrib/admin/#hooking-adminsite-instances-into-your-urlconf

urlpatterns = patterns('',
                       url(r'^$', direct_to_template, {'template_name': 'main/home.html'}, name='mai_main'),
                       (r'^jsi18n/$', 'django.views.i18n.javascript_catalog', {'packages': ('web_service',), }),
                       (r'', include('web_service.urls.guest')),
                       (r'', include('web_service.urls.user')),
                       (r'', include('web_service.urls.admin')),)


# if settings.DEBUG:
urlpatterns += patterns('',
                        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
                        # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
                        # to INSTALLED_APPS to enable admin documentation:
                        (r'^admin/doc/', include('django.contrib.admindocs.urls')),
                        # Uncomment the next line to enable the admin:
                        (r'^admin/', include(admin_page.site.urls)),
                        )

handler404 = bad_request
handler500 = server_error