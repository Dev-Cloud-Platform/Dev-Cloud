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
from django.views.generic.list import ListView
from core.settings.config import VM_IMAGE_ROOT_PASSWORD
from database.models.applications import Applications

JAVA = 'java'
NODEJS = 'node'
PHP = 'php'
PYTHON = 'python'
RUBY = 'ruby'
PREDEFINED = 'predefined'


class TechnologyBuilder(ListView):
    model = Applications

    def __java_configuration(self):
        """
        Generates configuration for java.
        @return: java configuration.
        """
        application_servers = self.get_list_application_servers("tomcat")
        cache = self.get_list_application_cache("memcached")
        sql = self.get_list_application_SQL("mysql", "mariadb", "postgresql")
        nosql = self.get_list_application_NoSQL("mongodb", "cassandra")

        return dict(application_servers.items() + cache.items() + sql.items() + nosql.items())

    def __nodejs_configuration(self):
        """
        Generates configuration for Node.JS.
        @return: Node.JS configuration.
        """
        application_servers = self.get_list_application_servers("node-app")
        cache = self.get_list_application_cache("memcached")
        sql = self.get_list_application_SQL("mysql", "mariadb", "postgresql")
        nosql = self.get_list_application_NoSQL("mongodb", "cassandra")

        return dict(application_servers.items() + cache.items() + sql.items() + nosql.items())

    def __php_configuration(self):
        """
        Generates configuration for php.
        @return: php configuration.
        """
        application_servers = self.get_list_application_servers("apache2", "nginx", "zend-server")
        cache = self.get_list_application_cache("memcached")
        sql = self.get_list_application_SQL("mysql", "mariadb", "postgresql")
        nosql = self.get_list_application_NoSQL("mongodb", "cassandra")

        return dict(application_servers.items() + cache.items() + sql.items() + nosql.items())

    def __python_configuration(self):
        application_servers = self.get_list_application_servers("apache2", "python-django")
        cache = self.get_list_application_cache("memcached")
        sql = self.get_list_application_SQL("mysql", "mariadb", "postgresql")
        nosql = self.get_list_application_NoSQL("mongodb", "cassandra")

        return dict(application_servers.items() + cache.items() + sql.items() + nosql.items())

    def __ruby_configuration(self):
        """
        Generates configuration for ruby.
        @return: ruby configuration.
        """
        application_servers = self.get_list_application_servers("apache2", "nginx", "rails")
        cache = self.get_list_application_cache("memcached")
        sql = self.get_list_application_SQL("mysql", "mariadb", "postgresql")
        nosql = self.get_list_application_NoSQL("mongodb", "cassandra")

        return dict(application_servers.items() + cache.items() + sql.items() + nosql.items())

    def extracts(self, technology):
        """
        Extracts available applications for given technology.
        @param technology: Given technology to extract.
        @return: Filtered applications for given technology.
        """
        if technology == JAVA:
            response = self.__java_configuration()
        elif technology == NODEJS:
            response = self.__nodejs_configuration()
        elif technology == PHP:
            response = self.__php_configuration()
        elif technology == PYTHON:
            response = self.__python_configuration()
        elif technology == RUBY:
            response = self.__ruby_configuration()
        else:
            return None

        return response

    @staticmethod
    def get_list_application_servers(*args):
        """
        Gets list for application servers.
        @param args:
        @return: list of application servers.
        """
        application_server_list = []

        for application_server in args:
            application_server_list.append(application_server)

        return {'applications_server': application_server_list}

    @staticmethod
    def get_list_application_cache(*args):
        """
        Gets list for application caches.
        @param args:
        @return: list of application caches.
        """
        application_cache_list = []

        for application_cache in args:
            application_cache_list.append(application_cache)

        return {'applications_cache': application_cache_list}

    @staticmethod
    def get_list_application_SQL(*args):
        """
        Gets list for database SQL application.
        @param args:
        @return: list of database SQL application.
        """
        application_SQL_list = []

        for application_SQL in args:
            application_SQL_list.append(application_SQL)

        return {'applications_SQL': application_SQL_list}

    @staticmethod
    def get_list_application_NoSQL(*args):
        """
        Gets list for database NoSQL application.
        @param args:
        @return: list of database NoSQL application.
        """
        application_NoSQL_list = []

        for application_NoSQL in args:
            application_NoSQL_list.append(application_NoSQL)

        return {'applications_NoSQL': application_NoSQL_list}

    @staticmethod
    def run_extra_options(juju_instance):
        """
        Install and run predefined configuration for technology.
        @param juju_instance: Data about status of installing application
        @return: Procedure to run on virtual machine.
        """
        print str(juju_instance.__dict__)
        if juju_instance.name == 'juju-gui':
            command = 'echo ' + VM_IMAGE_ROOT_PASSWORD + \
                      '| sudo -S iptables -t nat -I PREROUTING ' \
                      '-p tcp -i eth0 --dport 80 -j DNAT --to ' + juju_instance.public_address + ':80 ' \
                                                                                                 '&& sudo iptables -t nat -I PREROUTING ' \
                                                                                                 '-p tcp -i eth0 --dport 443 -j DNAT --to ' + juju_instance.public_address + ':443 ' \
                                                                                                                                                                             '&& sudo iptables -A FORWARD -p tcp -d ' + juju_instance.public_address + ' --dport 80 -j ACCEPT' \
                                                                                                                                                                                                                                                       '&& sudo iptables -A FORWARD -p tcp -d ' + juju_instance.public_address + ' --dport 443 -j ACCEPT'
            return command

        else:
            return ''
