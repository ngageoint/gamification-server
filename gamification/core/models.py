# -*- coding: utf-8 -*-

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, as long as
# any reuse or further development of the software attributes the
# National Geospatial-Intelligence Agency (NGA) authorship as follows:
# 'This software (gamification-server)
# is provided to the public as a courtesy of the National
# Geospatial-Intelligence Agency.
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import json
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.datastructures import SortedDict
from django.db.models.signals import post_save
from django.db import models
from gamification.badges.models import ProjectBadge, ProjectBadgeToUser
from jsonfield import JSONField
from mptt.models import MPTTModel, TreeForeignKey


TRUE_FALSE = [(0, 'False'), (1, 'True')]


class ProjectBase(models.Model):
    """
    A generic model for GeoQ objects.
    """

    active = models.BooleanField(default=True, help_text='If checked, this project will be listed in the active list.')
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200, help_text='Name of the project.')
    description = models.TextField(help_text='Details of this project that will be listed on the viewing page.')
    updated_at = models.DateTimeField(auto_now=True)
    url = models.TextField(help_text='Project Information URL', null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True
        ordering = ('-created_at',)


class Team(MPTTModel):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    members = models.ManyToManyField(User, null=True, blank=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    order = models.IntegerField(default=0, null=True, blank=True, help_text='Optionally specify the order teams should appear. Lower numbers appear sooner. By default, teams appear in the order they were created.')
    date_created = models.DateTimeField(auto_now_add=True)

    background_color = models.CharField(max_length=50, null=True, blank=True, help_text='Optional - Color to use for background of all team badges')
    icon = models.ImageField(upload_to='badge_images', null=True, blank=True, help_text='Optional - Image to show next to team names')

    def __str__(self):
        return "%s (%s)" % (self.name, str(len(self.members.all())))

    def get_all_users(self, include_self=True):
        u = []
        if include_self:
            u += self.members.all()
        for team in self.get_descendants():
            u += team.members.all()

        return u

    class Meta:
        ordering = ['-order', '-date_created', 'id']

    class MPTTMeta:
        order_insertion_by = ['name']


class Project(ProjectBase):
    """
    Top-level organizational object.
    """

    THEMES = (
        ("", "None"),
        ("camping", "Camping"),
        ("camping2", "Camping Theme 2"),
        ("map", "Geospatial"),
    )

    private = models.BooleanField(default=False, help_text='If checked, hide this project from the list of projects and public badge APIs.')
    supervisors = models.ManyToManyField(User, blank=True, null=True, related_name="supervisors", help_text='Anyone other than site administrators that can add badges and update the site')
    teams = models.ManyToManyField(Team, blank=True, null=True)
    viewing_pass_phrase = models.CharField(max_length=200, null=True, blank=True, help_text='Phrase that must be entered to view this page.')
    project_closing_date = models.DateTimeField(null=True, blank=True, help_text='Date that project "closes" with countdown shown on project page. Badges can still be added after this.')
    visual_theme = models.CharField(max_length=20, default="none", choices=THEMES, help_text='Visual Theme used to style the project page')
    background_image = models.ImageField(upload_to='badge_images', null=True, blank=True, help_text='Optional - Override theme background with this image')

    properties = JSONField(null=True, blank=True, help_text='JSON key/value pairs associated with this object, e.g. {"badges_mode":"blue"}')

    query_token = models.CharField(max_length=200, null=True, blank=True, help_text='Token that must be entered by any server requesting data - not implemented yet.')
    allowed_api_hosts = models.TextField(null=True, blank=True, help_text='Comma-separated list of hosts (IPs or Hostnames) that can access this project via data requests - not implemented yet')

    @property
    def user_count(self):
        return User.objects.filter(projectbadgetouser__projectbadge__project=self).distinct().count()

    @property
    def badge_count(self):
        return ProjectBadgeToUser.objects.filter(projectbadge__project=self).count()

    def get_absolute_url(self):
        return reverse('project-list', args=[self.name])

class Points(models.Model):
    user = models.ForeignKey(User)
    projectbadge = models.ForeignKey(ProjectBadge)
    value = models.IntegerField(default=0)
    date_awarded = models.DateTimeField('date awarded',auto_now=True)
    description = models.CharField(max_length=200)

    def get_absolute_url(self):
        return reverse('points-list', args=[self.id])

    class Meta:
        verbose_name_plural = "Points"


class UserProfile(models.Model):
    """ from http://stackoverflow.com/questions/44109/extending-the-user-model-with-custom-fields-in-django; this is one mechanism for adding extra details (currently score for badges) to the User model """
    defaultScore = 1
    user = models.OneToOneField(User)
    score = models.IntegerField(default=defaultScore)

    def __str__(self):
          return "%s's profile" % self.user

def create_user_profile(sender, instance, created, **kwargs):
    if created:
       profile, created = UserProfile.objects.get_or_create(user=instance)

post_save.connect(create_user_profile, sender=User)

import sys
if not 'syncdb' in sys.argv[1:2] and not 'migrate' in sys.argv[1:2]:
    from meta_badges import *