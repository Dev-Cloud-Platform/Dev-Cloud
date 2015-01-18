#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    # This will make the python interpreter see your packages as web_service.whatever
    #os.chdir('..')

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web_service.settings.dev")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
