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

"""
@author Michał Szczygiel <michal.szczygiel@wp.pl>
"""

from __future__ import unicode_literals

from django.db import models


class Applications(models.Model):
    """
    @models{Applications}
    Applications is an entity representing a object of application to install.
    """
    id = models.IntegerField(primary_key=True)
    application_name = models.CharField(max_length=45)
    description = models.CharField(max_length=45, blank=True)
    memory = models.FloatField(blank=True, null=True)
    space = models.FloatField(blank=True, null=True)
    cpu = models.IntegerField(blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)
    instalation_procedure = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'Applications'
        # app_label = 'database'


    def __unicode__(self):
        """
        @return:{string} Application id
        """
        return str(self.id)