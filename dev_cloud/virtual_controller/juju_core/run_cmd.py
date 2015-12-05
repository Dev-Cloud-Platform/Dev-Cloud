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
import cmd
import os
import paramiko
import sys
from core.settings.config import SSH_KEY_PATH

sys.stderr = open('/dev/null')
sys.stderr = sys.__stderr__


class RunCommand(cmd.Cmd):
    """ Simple shell to run a command on the host """

    prompt = 'ssh > '

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.hosts = []
        self.connections = []

    def do_add_host(self, args):
        """add_host
        Add the host to the host list"""
        if args:
            self.hosts.append(args.split(','))
        else:
            print "usage: host "

    def do_connect(self, args):
        """Connect to all hosts in the hosts list"""
        for host in self.hosts:
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.load_host_keys(os.path.expanduser(SSH_KEY_PATH))
            client.set_missing_host_key_policy(
                paramiko.AutoAddPolicy())
            client.connect(host[0], username=host[1], password=host[2])
            self.connections.append(client)

            channel = client.invoke_shell()
            self.stdin = channel.makefile('wb')
            self.stdout = channel.makefile('rb')

    def do_run(self, command):
        """run
        Execute this command on all hosts in the list"""
        if command:

            self.stdin.write(command)
            print self.stdout.read()
            self.stdout.close()
            self.stdin.close()

            for host, conn in zip(self.hosts, self.connections):
                stdin, stdout, stderr = conn.exec_command(command)
                stdin.close()
                for line in stdout.read().splitlines():
                    print 'host: %s: %s' % (host[0], line)
        else:
            print "usage: run "

    def do_close(self, args):
        for conn in self.connections:
            conn.close()


if __name__ == '__main__':
    RunCommand().cmdloop()