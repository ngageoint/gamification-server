# -*- coding: utf-8 -*-

from datetime import datetime

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.conf import settings

from singleton_models.models import SingletonModel
#from gamification.core.models import Project

from signals import badge_awarded
from managers import BadgeManager

if hasattr(settings, 'BADGE_LEVEL_CHOICES'):
    LEVEL_CHOICES = settings.BADGE_LEVEL_CHOICES
else:
    LEVEL_CHOICES = (
        ("1", "Bronze"),
        ("2", "Silver"),
        ("3", "Gold"),
        ("4", "Diamond"),
    )

class Badge(models.Model):
    name = models.CharField(max_length=255)
    level = models.CharField(max_length=1, choices=LEVEL_CHOICES)    
    icon = models.ImageField(upload_to='badge_images', default='', null=True, blank=True )
    value = 1
    
    objects = BadgeManager()
    
    @property
    def meta_badge(self):
        from utils import registered_badges
        return registered_badges[self.id]
    
    @property
    def title(self):
        return self.name
    
    @property
    def description(self):
        return self.meta_badge.description
    
    def __unicode__(self):
        return u"%s" % self.name
    
    def get_absolute_url(self):
        return reverse('badge_detail', kwargs={'slug': self.id})

    class Meta:
        verbose_name_plural = "Badge Templates"


class ProjectBadge(models.Model):
    project = models.ForeignKey('core.Project')
    badge = models.ForeignKey('Badge')
    user = models.ManyToManyField(User, related_name="badges", through='ProjectBadgeToUser')
    name = models.CharField(max_length=255)
    description = models.TextField()
    created = models.DateTimeField(default=datetime.now)
    awardLevel = models.IntegerField(default=1)
    multipleAwards = models.BooleanField(default=True)
    tags = models.CharField(max_length=400, default='', null=True, blank=True, help_text='Tags associated with this badge. Use a few small words separated by commas.')

    @property
    def meta_badge(self):
        from utils import registered_badges
        return registered_badges[self.id]

    def award_to(self, user):
        #has_badge = self in user.badges.all()
        #if self.meta_badge.one_time_only and has_badge:
        #    return False
        
        ProjectBadgeToUser.objects.create(projectbadge=self, user=user)
                
        #badge_awarded.send(sender=self.meta_badge, user=user, badge=self)
        
        #Grr... deprecated for Django 1.4+
        #message_template = "You just got the %s Badge!"
        #user.message.success(message = message_template % self.title)
        
        return ProjectBadgeToUser.objects.filter(projectbadge=self, user=user).count()

    def number_awarded(self, user_or_qs=None):
        """
        Gives the number awarded total. Pass in an argument to
        get the number per user, or per queryset.
        """
        kwargs = {'badge':self}
        if user_or_qs is None:
            pass
        elif isinstance(user_or_qs, User):
            kwargs.update(dict(user=user_or_qs))
        else:
            kwargs.update(dict(user__in=user_or_qs))
        return ProjectBadgeToUser.objects.filter(**kwargs).count()

    def __str__(self):
        return self.name

class ProjectBadgeToUser(models.Model):
    projectbadge = models.ForeignKey(ProjectBadge)
    user = models.ForeignKey(User)
    created = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name_plural = "Awarded Badges"

class BadgeSettings(models.Model):
    awardLevel = models.IntegerField(default=1)
    multipleAwards = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Badge Settings"

