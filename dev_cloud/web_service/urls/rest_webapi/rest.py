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
from virtual_controller.api.views.application import ApplicationViewSet
from virtual_controller.api.views.installed_application import InstalledApplicationList
from virtual_controller.api.views.template_instances import TemplateInstancesViewSet
from virtual_controller.api.views.user import UserViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'applications', ApplicationViewSet)
router.register(r'template-instances', TemplateInstancesViewSet)
router.register(r'users', UserViewSet)
router.register(r'installed-applications', InstalledApplicationList)

# Example how to call:
# curl -i -H "Accept: application/json" -H "Content-Tyon/json"
# -X GET --data "username=<username>&password=<password>" http://127.0.0.1:8000/rest_api/users/admin-users/
# The API URLs are now determined automatically by the router.
urlpatterns = patterns('', url(r'^rest_api/', include(router.urls)),
                       url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')))
