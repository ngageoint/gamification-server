#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Description: Settings for default environment.
"""


from base import *


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "db",
        "PORT": "5432"
    }
}

CORS_ORIGIN_ALLOW_ALL = True
