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

from django.utils.http import int_to_base36, base36_to_int
from core.utils.exception import DevCloudException
from database.models import Users


class PasswordResetTokenGenerator(object):
    """
    Class for generating tokens during password reset.
    """

    @staticmethod
    def make_token(user):
        """
        @parameter{user,User} instance of the User whom Token should be
        generated for

        @returns{string} Token with timestamp generated for specified User
        """
        import hashlib

        h = hashlib.sha1(user.password +
                         unicode(user.last_activity) +
                         unicode(user.id)).hexdigest()[::2]
        return "%s-%s" % (int_to_base36(user.id), h)

    def check_token(self, user, token):
        """
        @parameter{user,User} instance of the User whose Token should be
        checked.
        @parameter{token,string} Token to check

        @returns{bool} @val{true} for right Token, @val{false} for wrong Token
        """
        try:
            ts_b36 = token.split("-")[0]
        except ValueError:
            return False

        try:
            uid = base36_to_int(ts_b36)
        except ValueError:
            return False

        # Check that the uid has not been tampered with
        if uid != user.id:
            return False

        if self.make_token(user) != token:
            return False

        return True


default_token_generator = PasswordResetTokenGenerator()


def check_token(user_id, token):
    """
    @clmview_guest
    @parameter{user_id} user for whom token should be checked
    @parameter{token} token to check

    @response None
    """
    try:
        user = Users.objects.get(id=user_id)
    except Exception:
        raise DevCloudException('user_get')

    if default_token_generator.check_token(user, int_to_base36(user_id) + u'-' + token):
        return
    raise DevCloudException('user_bad_token')


def set_password_token(user_id, token, new_password):
    """
    @clmview_guest
    @parameter{user_id} id of the User whose password should be set
    @parameter{token} token to set password
    @parameter{new_password,string} new password

    @response{dict} User's new data (if succeeded)
    """
    try:
        user = Users.objects.get(id=user_id)
    except Exception:
        raise DevCloudException('user_get')

    if default_token_generator.check_token(user, int_to_base36(user_id) + u'-' + token):
        user.password = new_password
        try:
            user.save()
        except Exception:
            raise DevCloudException('user_set_password')
    else:
        raise DevCloudException('user_bad_token')
    return user.dict
