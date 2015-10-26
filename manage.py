#!/usr/bin/env python

import os, sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gamification.settings.default")
    os.environ['PGCONNECT_TIMEOUT'] = '30'

    manage_dir = os.path.dirname(os.path.realpath(__file__))
    sys.path.append(os.path.join(manage_dir, 'gamification'))

    from django.core.management import execute_from_command_line
    import gamification.startup as startup
    startup.run()
    execute_from_command_line(sys.argv)
