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

class Users(models.Model):
    id = models.IntegerField(primary_key=True)
    login = models.CharField(unique=True, max_length=45)
    password = models.CharField(max_length=32)
    name = models.CharField(max_length=45, blank=True)
    lastname = models.CharField(max_length=45, blank=True)
    email = models.CharField(unique=True, max_length=255)
    create_time = models.DateTimeField(blank=True, null=True)
    language = models.CharField(max_length=45, blank=True)
    picture = models.FileField(blank=True)
    last_activity = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'Users'
        app_label = 'web_service'