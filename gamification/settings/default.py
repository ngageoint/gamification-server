#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Description: Settings for default environment.
"""


from base import *


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "gamification",
        "USER": "game_manager",
        "PASSWORD": "django-gamification",
        "HOST": "",
        "PORT": "5432"
    }
}

CORS_ORIGIN_WHITELIST = ('192.168.5.131:8000', 'localhost:8000',)
CORS_ALLOW_METHODS = ('GET', 'POST', 'OPTIONS')
