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
from rest_framework import serializers

from database.models import InstalledApplications


class InstalledApplicationsSerializer(serializers.ModelSerializer):

    class Meta:
        model = InstalledApplications
        fields = (
            'installed_app_id', 'workspace', 'clx_ip', 'public_port', 'private_port', 'user', 'application',
            'virtual_machine')


