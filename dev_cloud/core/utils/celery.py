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
import os

from celery import Celery
from django.conf import settings
from core.settings.common import BROKER_URL, CELERY_RESULT_BACKEND

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.common')

app = Celery('dev_cloud.virtual_controller.celery', broker=BROKER_URL, backend=CELERY_RESULT_BACKEND, include=['virtual_controller.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
    )

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('core.settings.common') #django.conf:settings
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)