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

from django_assets import Bundle, register
# ----------------------------------------------------------------------------------------------------------------------
js = Bundle('../assets/dist/scripts/vendor.js',
            '../assets/dist/scripts/ui.js',
            '../assets/dist/scripts/app.js', output='gen/packed.js')
register('template_js', js)

css = Bundle('../assets/dist/bower_components/font-awesome/css/font-awesome.min.css',
             '../assets/dist/bower_components/weather-icons/css/weather-icons.min.css',
             '../assets/dist/styles/main.css', output='gen/packed.css')
register('template_css', css)
# ----------------------------------------------------------------------------------------------------------------------
