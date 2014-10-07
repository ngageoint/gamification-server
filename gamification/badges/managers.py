# -*- coding: utf-8 -*-

from django.db import models

class BadgeManager(models.Manager):
    def active(self):
        import badges
        return self.get_query_set().filter(id__in=badges.registered_badges.keys())
        