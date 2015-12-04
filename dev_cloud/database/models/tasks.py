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
from database.models import Users

POSTS_PER_PAGE = 25  # Show 25 tasks per page


class TaskManager(models.Manager):
    def get_page(self, user, task_id):
        page = None

        try:
            create_time = self.filter(user__id=user).filter(id=task_id)
            page = self.filter(user__id=user).filter(
                create_time__gt=create_time[0].create_time).count() / POSTS_PER_PAGE + 1
        except IndexError:
            pass

        return page


class Tasks(models.Model):
    id = models.AutoField(primary_key=True)
    task_name = models.CharField(max_length=255)
    is_processing = models.IntegerField(blank=True)
    create_time = models.DateTimeField(blank=True, null=True)
    is_read = models.IntegerField(blank=True)
    is_succeeded = models.IntegerField(blank=True)
    user = models.ForeignKey(Users)
    objects = TaskManager()

    class Meta:
        managed = False
        db_table = 'Tasks'
        # app_label = 'database'
