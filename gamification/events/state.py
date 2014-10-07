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

from django.core.exceptions import ObjectDoesNotExist
from gamification.badges.models import ProjectBadge, ProjectBadgeToUser

class State(object):
    """
    A State is a collection of event data (associated with a user and project)
    that will be submitted to the rules engine for reasoning.
    """
    
    def __init__(self, user, project, projectbadge, event_data):
        self._user = user
        self._project = project
        self._projectbadge = projectbadge
        self._event_data = event_data # A dictionary of dictionaries
    
    @property
    def user(self):
        return self._user
    
    @property
    def project(self):
        return self._project
    
    @property
    def event_data(self):
        return self._event_data
    
    @event_data.setter
    def event_data(self, event_data):
        self._event_data = event_data
        
    # Awards a project badge to a user (if the user does not yet have the badge)    
    def award(self, user, project):
        project_badge = self._projectbadge
        project_badge.award_to(user)