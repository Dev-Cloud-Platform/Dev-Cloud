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
from rest_framework import permissions
from core.utils.auth import authenticate


class UsersPermission(permissions.BasePermission):
    """
    Permissions for UsersViewSet
    """
    def has_permission(self, request, view):
        username = request.DATA.get('username', None) or request.query_params.get('username', None)
        password = request.DATA.get('password', None) or request.query_params.get('password', None)

        user = authenticate(username, password)

        if user:
            return True

        return False
