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

from template_instances import TemplateInstances


class VirtualMachines(models.Model):
    id = models.AutoField(primary_key=True)
    vm_id = models.IntegerField(blank=True)
    ctx = models.CharField(max_length=45, blank=True)
    disk_space = models.CharField(max_length=45, blank=True)
    public_ip = models.CharField(max_length=45, blank=True)
    private_ip = models.CharField(max_length=45, blank=True)
    template_instance = models.ForeignKey(TemplateInstances)

    class Meta:
        managed = False
        db_table = 'Virtual_machines'
        # app_label = 'database'