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
from __future__ import absolute_import

from celery import group
from djcelery import celery
from core.utils.celery import app

Global_i = 1

@celery.task
def add(x, y):
    return x + y


@app.task(trail=True)
def sleeptask(i):
    from time import sleep
    sleep(i)
    print Global_i + Global_i
    return add(2, 3)


@app.task(trail=True)
def A(how_many):
    print group(B.s(i) for i in range(how_many))()
    return group(B.s(i) for i in range(how_many))()

@app.task(trail=True)
def B(i):
    return pow2.delay(i)

@app.task(trail=True)
def pow2(i):
    return i ** 2