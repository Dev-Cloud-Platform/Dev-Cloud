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

from django.contrib import admin

from models.applications import Applications

from models.installed_applications import InstalledApplications
from models.roles import Roles
from models.template_instances import TemplateInstances
from models.users import Users
from models.users_roles import UsersInRoles
from models.virtual_machines import VirtualMachines

admin.site.register(Applications)
admin.site.register(InstalledApplications)
admin.site.register(Roles)
admin.site.register(TemplateInstances)
admin.site.register(Users)
admin.site.register(UsersInRoles)
admin.site.register(VirtualMachines)
