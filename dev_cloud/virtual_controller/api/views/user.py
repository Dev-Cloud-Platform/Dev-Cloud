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
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response
from database.models import Users
from virtual_controller.api.permissions import base_permissions as api_permissions
from virtual_controller.api.serializers.users_serializer import UserSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed.
    """
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    permission_classes = {api_permissions.UsersPermission}

    @list_route(methods=['get'], url_path='admin-users')
    def admin_users(self, request):
        """
        Gets list of admin users.
        @param request:
        @return: List of admin users.
        """
        admin_users = Users.objects.get(is_superuser=True)
        serializer = self.get_serializer(admin_users)
        return Response(serializer.data)
