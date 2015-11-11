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
"""
WSGI config for web_service project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""
# from core.settings.config import ENVIROMENT_PATH
#
# activate_this = ENVIROMENT_PATH
# execfile(activate_this, dict(__file__=activate_this))

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.prod")
os.environ["CELERY_LOADER"] = "django"

import djcelery
djcelery.setup_loader()

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

