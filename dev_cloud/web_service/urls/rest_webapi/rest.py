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
from django.conf.urls import patterns, url, include
from rest_framework.routers import DefaultRouter
from virtual_controller.views import application
from virtual_controller.views.user import UserViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'users', UserViewSet)

application_patterns = patterns('virtual_controller.views.application',
                                url(r'^applications/$', application.ApplicationList.as_view()))
                                # Example how to call:
                                # curl -i -H "Accept: application/json" -H "Content-Tyon/json"
                                # -X GET http://127.0.0.1:8000/rest_api/applications/

# The API URLs are now determined automatically by the router.
urlpatterns = patterns('',
                       url(r'^rest_api/', include(router.urls)),
                       url(r'^rest_api/', include(application_patterns)))
