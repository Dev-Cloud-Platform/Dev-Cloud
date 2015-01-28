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
from core.utils.exception import DevCloudException


class Users(models.Model):
    id = models.IntegerField(primary_key=True)
    login = models.CharField(unique=True, max_length=45)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=45, blank=True)
    lastname = models.CharField(max_length=45, blank=True)
    email = models.CharField(unique=True, max_length=255)
    create_time = models.DateTimeField(blank=True, null=True)
    language = models.CharField(max_length=45, blank=True)
    picture = models.FileField(blank=True)
    activation_key = models.CharField(max_length=255, blank=True)
    is_active = models.IntegerField(blank=True)
    is_superuser = models.IntegerField(blank=True)
    last_activity = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Users'
        # app_label = 'database'


    @property
    def dict(self):
        """
        @returns{dict} this User's data
        \n fields:
        @dictkey{user_id,int} id of this User
        @dictkey{first,string} first name
        @dictkey{last,string} last name
        @dictkey{login,string} login
        @dictkey{email,string} email
        @dictkey{act_key,string} activation key's content
        @dictkey{is_active,bool} true for active User
        @dictkey{is_superuser,bool} true for User with admin privilidges
        @dictkey{activation_date,datetime.datetime} activation's date
        @dictkey{last_login_date,datetime.datetime} last login's date
        """
        d = {}
        d['user_id'] = self.id
        d['first'] = self.name
        d['last'] = self.lastname
        d['login'] = self.login
        d['email'] = self.email
        d['act_key'] = self.activation_key or ''
        d['is_active'] = self.is_active or 0
        d['is_superuser'] = self.is_superuser or 0
        d['activation_date'] = self.create_time or ''
        d['last_login_date'] = self.last_activity or ''
        return d

    @property
    def short_dict(self):
        """
        @returns{dict} very short version of User's data
        \n fields:
        @dictkey{user_id,int} id of this User
        @dictkey{first,string} first name
        @dictkey{last,string} last name
        """
        d = {}
        d['user_id'] = self.id
        d['first'] = self.name
        d['last'] = self.lastname

        return d

    @staticmethod
    def superuser(user_id):
        """
        @raises{user_permission,DevCloudException} User isn't superuser
        @param user_id: User's id, int
        @return: {bool}
        @avail{True} - User is superuser

        @raises{user_permission,DevCloudException} User isn't superuser
        """
        user = Users.get(user_id)
        if not user.is_superuser:
            raise DevCloudException('user_permission')
        return True