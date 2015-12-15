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


class JujuInstance(object):
    """
    http://dirtsimple.org/2004/12/python-is-not-java.html
        ~Trying break my mind.
    """

    def __init__(self):
        self._name = None
        self._units = None
        self._unit_machines = None
        self._num_of_units = None
        self._open_ports = None
        self._machine = None
        self._agent_state = None
        self._public_address = None
        self._instance_id = None
        self._machine_number = None
        self._exposed = None
        self._unit_plural = None
        self._relations = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def units(self):
        return self._units

    @units.setter
    def units(self, units):
        self._units = units

    @property
    def unit_machines(self):
        return self._unit_machines

    @unit_machines.setter
    def unit_machines(self, unit_machines):
        self._unit_machines = unit_machines

    @property
    def num_of_units(self):
        return self._num_of_units

    @num_of_units.setter
    def num_of_units(self, num_of_units):
        self._num_of_units = num_of_units

    @property
    def open_ports(self):
        return self._open_ports

    @open_ports.setter
    def open_ports(self, open_ports):
        self._open_ports = open_ports

    @property
    def machine(self):
        return self._machine

    @machine.setter
    def machine(self, machine):
        self._machine = machine

    @property
    def agent_state(self):
        return self._agent_state

    @agent_state.setter
    def agent_state(self, agent_state):
        self._agent_state = agent_state

    @property
    def public_address(self):
        return self._public_address

    @public_address.setter
    def public_address(self, public_address):
        self._public_address = public_address

    @property
    def instance_id(self):
        return self._instance_id

    @instance_id.setter
    def instance_id(self, instance_id):
        self._instance_id = instance_id

    @property
    def machine_number(self):
        return self._machine_number

    @machine_number.setter
    def machine_number(self, machine_number):
        self._machine_number = machine_number

    @property
    def exposed(self):
        return self._exposed

    @exposed.setter
    def exposed(self, exposed):
        self._exposed = exposed

    @property
    def unit_plural(self):
        return self._unit_plural

    @unit_plural.setter
    def unit_plural(self, unit_plural):
        self._unit_plural = unit_plural

    @property
    def relations(self):
        return self._relations

    @relations.setter
    def relations(self, relations):
        self._relations = relations
