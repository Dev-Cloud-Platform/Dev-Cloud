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
import sys
import select
import time

import paramiko

from core.settings.config import SSH_KEY_PATH
from core.utils.log import info, error

sys.stderr = open('/dev/null')
sys.stderr = sys.__stderr__


class RunRemoteCommand(object):
    """
    Simple shell to run a command on the host
    """

    def __init__(self, host, user, key, password):
        # cmd.Cmd.__init__(self)
        self.host = host
        self.user = user
        self.key = key
        self.password = password
        self.client = None

    def __connect(self):
        """
        Connect to all hosts in the hosts list
        """
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.load_host_keys(os.path.expanduser(SSH_KEY_PATH))
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(self.host, username=self.user, password=self.password)

    def run(self, *commands):
        """
        Execute this command on all hosts in the list
        @param command: command to run on ssh server.
        @return:
        """

        if commands:
            i = 1
            # Try to connect to the host. Retry a few times if it fails.
            while True:
                info(None, "Trying to connect to %s (%i/30)" % (self.host, i))
                try:
                    self.__connect()
                    info(None, "Connected to %s" % self.host)
                    break
                except paramiko.AuthenticationException:
                    error(None, "Authentication failed when connecting to %s" % self.host)
                    sys.exit(1)
                except:
                    error(None, "Could not SSH to %s, waiting for it to start" % self.host)
                    i += 1
                    time.sleep(2)

                # If we could not connect within time limit
                if i == 30:
                    error(None, "Could not connect to %s. Giving up" % self.host)
                    sys.exit(1)

            # Send the command (non-blocking)
            for command in commands:
                stdin, stdout, stderr = self.client.exec_command(command)

                # Wait for the command to terminate
                while not stdout.channel.exit_status_ready():
                    # Only print data if there is data to read in the channel
                    if stdout.channel.recv_ready():
                        rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
                        if len(rl) > 0:
                            # Print data from stdout
                            print stdout.channel.recv(1024),
                            info(None, stdout.channel.recv(1024))
        else:
            raise Exception

    def __close_connection(self):
        """
        Disconnect from the host
        """
        info(None, "Command done, closing SSH connection")
        self.client.close()
