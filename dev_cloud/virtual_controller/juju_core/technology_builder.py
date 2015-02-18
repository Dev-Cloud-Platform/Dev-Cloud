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
from database.models.applications import Applications

JAVA = 'java'
NODEJS = 'node'
PHP = 'php'
PYTHON = 'python'
RUBY = 'ruby'


class TechnologyBuilder(ListView):

    model = Applications

    def __java_configuration(self):
        """
        Generates configuration for java.
        @return: java configuration.
        """
        return None

    def __nodejs_configuration(self):
        """
        Generates configuration for Node.JS.
        @return: Node.JS configuration.
        """
        return None

    def __php_configuration(self):
        """
        Generates configuration for php.
        @return: php configuration.
        """
        application_servers = self.getListApplicationServers("apache2")
        cache = self.getListApplicationCache("memcached")
        sql = self.getListApplicationSQL("mysql")
        nosql = self.getListApplicationNoSQL("mongodb")

        return dict(application_servers.items() + cache.items() + sql.items() + nosql.items())

    def __python_configuration(self):
        """
        Generates configuration for python.
        @return: python configuration.
        """
        return None

    def __ruby_configuration(self):
        """
        Generates configuration for ruby.
        @return: ruby configuration.
        """
        return None

    def extracts(self, technology):
        """
        Extracts available applications for given technology.
        @param technology: Given technology to extract.
        @return: Filtered applications for given technology.
        """
        response = {}

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
    def getListApplicationServers(*args):
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
    def getListApplicationCache(*args):
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
    def getListApplicationSQL(*args):
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
    def getListApplicationNoSQL(*args):
        """
        Gets list for database NoSQL application.
        @param args:
        @return: list of database NoSQL application.
        """
        application_NoSQL_list = []

        for application_NoSQL in args:
            application_NoSQL_list.append(application_NoSQL)

        return {'applications_NoSQL': application_NoSQL_list}
