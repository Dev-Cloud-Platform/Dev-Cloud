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
import ast
from django.utils.translation import ugettext as _
from core.utils import log


def debug(logger_id, data):
    pass


def info(logger_id, data):
    pass


def warning(logger_id, data):
    pass


def exception(logger_id, data):
    pass


def error(logger_id, data):
    """
    Special error logger for reduce amount of code, which analyze a status and return proper log.
    @param logger_id: optional, id of the logger. If no id is provided, logs are anonymous.
    @param data: content of the log.
    """
    if data.status_code == 200:
        log.error(logger_id, _("CC1 - Problem with request: ") + data.url
                  + _(" obtain problem: ") + ast.literal_eval(data.text)).get("data")
    else:
        log.error(logger_id, _("CC1 - Problem with request: ") + data.url)