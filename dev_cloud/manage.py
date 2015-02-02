#!/usr/bin/env python

# -*- coding: utf-8 -*-
# @COPYRIGHT_begin
#
# Copyright [2015] Michal Szczygiel, M4GiK Software
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
import sys

if __name__ == "__main__":
    # This will make the python interpreter see your packages as dev_cloud.whatever
    # os.chdir('..')

    if len(sys.argv) < 2:
        print 'Usage ./manage.py <manager> <args>'
        sys.exit(1)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.%s" % sys.argv[1])

    from django.core.management import execute_from_command_line
    args = sys.argv[:]
    args.pop(1)

    execute_from_command_line(args)
