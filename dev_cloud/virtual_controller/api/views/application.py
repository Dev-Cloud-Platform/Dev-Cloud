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
from rest_framework import viewsets, status
from rest_framework.decorators import list_route
from rest_framework.response import Response

from database.models import Applications
from virtual_controller.api.serializers.applications_serializer import ApplicationsSerializer


class ApplicationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows display list of all available applications.
    """
    queryset = Applications.objects.all()
    serializer_class = ApplicationsSerializer

    @list_route(methods=['get'], url_path='get-application')
    def get_application(self, request):
        """
        You need add payload with key application and your application name as value.
        Example: GET /rest_api/applications/get-application/?application=mysql
        @param request:
        @return:
        """
        application = request.DATA.get('application', None) or request.query_params.get('application', None)
        if application:
            get_application = Applications.objects.get(application_name=application)
            serializer = self.get_serializer(get_application)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)





