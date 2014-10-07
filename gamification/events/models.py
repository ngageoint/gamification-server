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
import datetime
from django.contrib.auth.models import User
from gamification.core.models import Project, ProjectBadge
from django.db import models

class Event(models.Model):
    """
    An Event is an action reported by an external system
    """

    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    event_dtg = models.DateTimeField('event date')
    details = models.TextField(editable=False)

    def __init__(self, *args, **kw):
        # dictionary for the details of the event
        self.details_map = {}
        super(Event, self).__init__(*args, **kw)
        if self.details:
            try:
                self.details_map = json.loads(self.details)
            except TypeError:
                self.details_map = self.details

    def save(self, *args, **kw):
        self.details = json.dumps(self.details_map)
        super(Event, self).save(*args, **kw)

    @property
    def dtg(self):
        return self.event_dtg

    @property
    def details_map(self):
        return self._details_map
    
    @details_map.setter
    def details_map(self, details_map):
        self._details_map = details_map
        
    @property
    def state(self):
        return self._state
    
    @state.setter
    def state(self, state):
        self._state = state

    @property
    def is_current_event(self):
        return self._current_event

    @property
    def is_today(self):
        return datetime.datetime.date() == event_dtg.date()

    @state.setter
    def current_event(self, current_event_id):
        self._current_event = (self.id == current_event_id)

    # Adds specified event data to the state    
    def update_state(self, outer_key, inner_key, inner_value):
        try:
            if not outer_key in self._state.event_data:
                self._state._event_data[outer_key] = {}
            self._state._event_data[outer_key][inner_key] = inner_value 
        except AttributeError:
            print 'AttributeError'
            pass

class Policy(models.Model):
    """
    A Policy is a condition - action specifier for the rules engine. Will include 1 or more Rules
    """

    STATE_POLICY = 0
    AWARD_POLICY = 1
    POLICY_CHOICES = ( (STATE_POLICY, 'State Policy'), (AWARD_POLICY, 'Award Policy'), )

    project = models.ForeignKey(Project)
    projectbadge = models.ForeignKey(ProjectBadge)
    type = models.IntegerField(choices=POLICY_CHOICES)
    rule = models.TextField()

    def __unicode__(self):
        try:
            kind = self.POLICY_CHOICES[self.projectbadge.type][1]
        except:
            kind = 'Policy'
        return u"%s for %s on %s" % (kind, self.projectbadge.name, self.project.name)


#class Rule(models.Model):
#    """
#    A Rule is a decision specifier that will be the basis for a Policy
#    """
#
#    name = models.CharField(max_length=100)
#    policy = models.ForeignKey(Policy)
#    badge = models.ForeignKey(ProjectBadge)
#    conditions = models.TextField(editable=False)
#
#    def __init__(self, *args, **kw):
#        # dictionary for the details of the event
#        self.conditions_list = []
#        super(Event, self).__init__(*args, **kw)
#        if self.conditions:
#            self.conditions_list = json.loads(self.conditions)
#
#    def save(self, *args, **kw):
#        self.conditions = json.dumps(self.conditions_list)
#        super(Event, self).save(*args, **kw)