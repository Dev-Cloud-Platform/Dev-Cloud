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

from __future__ import unicode_literals

from django.db import models

from roles import Roles
from users import Users


class UsersInRoles(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users)
    role = models.ForeignKey(Roles)

    class Meta:
        managed = False
        db_table = 'Users_in_roles'
        # app_label = 'database'