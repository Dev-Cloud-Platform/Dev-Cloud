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
    picture = models.ImageField(blank=True, upload_to='pictures')
    activation_key = models.CharField(max_length=255, blank=True)
    is_active = models.IntegerField(blank=True)
    is_superuser = models.BooleanField(blank=True)
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
        @dictkey{picture, path} path to image
        @dictkey{act_key,string} activation key's content
        @dictkey{is_active,bool} true for active User
        @dictkey{is_superuser,bool} true for User with admin privilidges
        @dictkey{activation_date,datetime.datetime} activation's date
        @dictkey{last_activity,datetime.datetime} last login's date
        """
        d = {'user_id': self.id, 'first': self.name, 'last': self.lastname, 'login': self.login, 'email': self.email,
             'picture': self.picture, 'act_key': self.activation_key or '', 'is_active': self.is_active or 0,
             'is_superuser': self.is_superuser or 0, 'activation_date': self.create_time or '',
             'last_activity': self.last_activity or ''}
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
        d = {'user_id': self.id, 'first': self.name, 'last': self.lastname}

        return d

    @staticmethod
    def get(user_id):
        """
        @parameter{id,int} primary index of the @type{User}
        @returns{User} instance of requested @type{User}
        @raises{user_get,CLMException}
        """
        try:
            user = Users.objects.get(pk=user_id)
        except:
            raise DevCloudException('user_get')
        return user

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

    def set_password(self, password):
        self.password = password

    def delete(self, *args, **kwargs):
        self.picture.delete()
        super(Users, self).delete(*args, **kwargs)

    @staticmethod
    def save_picture(user, request):
        session = request.session
        upload_picture = request.FILES['image']
        if user.picture is not None:
            user.picture.delete()
        user.picture.save(upload_picture.name, upload_picture)
        session['picture_id'] = user.id

    @staticmethod
    def parse_user(user):
        """
        Helper function that returns \c User object based on the provided dictionary.
        @param user:
        @return:
        """
        return Users(id=user['user_id'], name=user['first'], lastname=user['last'], login=user['login'],
                     password='', email=user['email'], is_active=user['is_active'], is_superuser=user['is_superuser'])