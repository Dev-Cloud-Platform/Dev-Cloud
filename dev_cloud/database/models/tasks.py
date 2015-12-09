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

    @property
    def dict(self):
        """
        @returns{dict} this User's data
        \n fields:
        @dictkey{id, int} id of this Task
        @dictkey{task_name, string} task name
        @dictkey{is_processing, int} status of processing this task
        @dictkey{create_time, datetime.datetim} create's date
        @dictkey{is_read, int} status about read this task
        @dictkey{is_succeeded, int} the status of the successful completion Task
        @dictkey{user, int} user id FK
        """
        d = {'id': self.id, 'task_name': self.task_name, 'is_processing': self.is_processing or 0,
             'create_time': self.create_time, 'is_read': self.is_read or '',
             'is_succeeded': self.is_succeeded or '', 'user': self.activation_key or ''}
        return d
