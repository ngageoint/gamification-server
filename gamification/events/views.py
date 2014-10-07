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

from dateutil.parser import parse
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import ObjectDoesNotExist
from gamification.core.models import Project
from gamification.events.models import Event,Policy
from gamification.events.state import State
from gamification.badges.models import ProjectBadge, ProjectBadgeToUser
from intellect.Intellect import Intellect
import json
import logging, sys

# For debug
from datetime import datetime

def assign_badge(request, *args, **kwargs):
    is_admin = request.user.is_superuser or request.user.groups.filter(name='admin_group').count() > 0
    if not is_admin:
        return HttpResponse('{"status":"Aborted", "error":"Unauthorized"}', mimetype="application/json", status=401)

    # Get user and project
    user = get_object_or_404(User,username=kwargs['username'])
    badge = get_object_or_404(ProjectBadge,id=kwargs['badge'])
    event_dtg = timezone.now()

    try:
        current_badge = ProjectBadgeToUser(user=user, projectbadge=badge, created=event_dtg)
        current_badge.save()
    except ValueError, ve:
        #print('handle_event failed create event: {0}').format(ve)
        return HttpResponse('{"status":"Invalid Badge Creation","error":"'+str(ve)+'"}', mimetype="application/json", status=500)

    return HttpResponse('{"status":"Badge Created", "id":'+str(current_badge.id)+'}', mimetype="application/json", status=200)



def handle_event(request, *args, **kwargs):
    if request.method == 'POST':

        data = json.loads(request.body)

        # Get user and project
        user = get_object_or_404(User,username=kwargs['username'])
        project = get_object_or_404(Project,name=kwargs['projectname'])
        
        # Get event DTG
        try:
            event_dtg_str = data['event_dtg']
            try:
                event_dtg = parse(event_dtg_str)
            except ValueError:
                return HttpResponse('Invalid event_dtg', status=400)      
        except MultiValueDictKeyError:
            event_dtg = timezone.now()
        #print('handle_event got event_dtg {0}').format(datetime.strftime(event_dtg, '%Y-%m-%dT%H:%M:%S%Z'))
        
        # Get event details
        try:
            details = data['details']
        except MultiValueDictKeyError:
            details = None
        #print('handle_event got details {0}').format(details)
        
        # Create Event object
        try:
            current_event = Event(user=user, project=project, event_dtg=event_dtg, details=details)
        except ValueError, ve:
            #print('handle_event failed create event: {0}').format(ve)
            return HttpResponse('Invalid event', status=400) # If, for example, 'details' JSON does not load   
        
        # Save Event object
        current_event.save()

        #####################################################################
        # 'Training' demo policies. Assumes there is a 'training' project with badge id 1. Badge awarded when all courses finished.
        # Sample curl command for sending event for user 'admin': 
        # curl -d "details={\"event_type\":\"course_complete\",\"course_id\":\"008031\"}" http://localhost:8000/users/admin/projects/training/event/
        #state_policy = "from gamification.events.models import Event\nrule 'Rule 1':\n\twhen:\n\t\t$event := Event(('event_type' in details_map) and ('course_complete' in details_map['event_type']) and ('course_id' in details_map))\n\tthen:\n\t\t$event.update_state('course_complete', $event.details_map['course_id'], $event.event_dtg)\n"
        #award_policy = "from gamification.events.state import State\nrule 'Rule 1':\n\twhen:\n\t\t$state := State((project.name == 'training') and ('course_complete' in event_data) and ('008031' in event_data['course_complete']) and ('008189' in event_data['course_complete']) and ('008582' in event_data['course_complete']) and ('009446' in event_data['course_complete']) and ('013413' in event_data['course_complete']) and ('013567' in event_data['course_complete']) and ('016003' in event_data['course_complete']) and ('016094' in event_data['course_complete']) and ('017724' in event_data['course_complete']) and ('020146' in event_data['course_complete']) and ('023416' in event_data['course_complete']))\n\tthen:\n\t\t$state.award($state.user, $state.project, 1)\n"
        #####################################################################

        #####################################################################
        # 'GeoQ AOI' demo policies. Assumes there is a 'geoq' project with badge id 4. Badge awarded when at least three AOIs are completed.
        # Sample curl command for sending event for user 'admin':
        # curl -d "details={\"event_type\":\"aoi_complete\",\"aoi_id\":\"2\"}" http://localhost:8000/users/admin/projects/geoq/event/
        #bronze_state_policy = "from gamification.events.models import Event\nrule 'Rule 1':\n\twhen:\n\t\t$event := Event((" + str(current_aoi) + " == details_map['aoi_id']) and ( details_map['feature_count'] > 0))\n\tthen:\n\t\t$event.update_state('aoi_complete', $event.details_map['aoi_id'], $event.event_dtg)\n"
        #bronze_award_policy = "from gamification.events.state import State\nrule 'Rule 1':\n\twhen:\n\t\t$state := State((project.name == 'django_geoq') and ('aoi_complete' in event_data) and (len(event_data['aoi_complete']) > 0))\n\tthen:\n\t\t$state.award($state.user, $state.project, 6)\n"
        #silver_state_policy = "from gamification.events.models import Event\nrule 'Rule 1':\n\twhen:\n\t\t$event := Event(('event_type' in details_map) and ('aoi_complete' in details_map['event_type']) and ('aoi_id' in details_map) and ( details_map['feature_count'] > 0))\n\tthen:\n\t\t$event.update_state('aoi_complete', $event.details_map['aoi_id'], $event.event_dtg)\n"
        #silver_award_policy = "from gamification.events.state import State\nrule 'Rule 1':\n\twhen:\n\t\t$state := State((project.name == 'django_geoq') and ('aoi_complete' in event_data) and (len(event_data['aoi_complete']) % 3 == 0) and (" + str(current_aoi) + " in event_data['aoi_complete']))\n\tthen:\n\t\t$state.award($state.user, $state.project, 5)\n"

        #policies = [[bronze_state_policy, bronze_award_policy], [silver_state_policy, silver_award_policy]]

        #####################################################################

        logger = logging.getLogger('intellect')
        logger.setLevel(logging.DEBUG)
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s%(message)s'))
        logger.addHandler(consoleHandler)

        # get badges for this project, then for each badge run through its policies
        project_badges = ProjectBadge.objects.filter(project=project)

        for badge in project_badges:
            policies = Policy.objects.filter(project=project,projectbadge=badge)
            # make sure we have policies
            if policies.count() == 2:
                try:
                    state_policy = policies.get(type=Policy.STATE_POLICY)
                    intellect = Intellect()
                    intellect.learn(state_policy.rule)
                    events = Event.objects.filter(user=user,project=project)
                    event_data = {}
                    state = State(user,project,badge,event_data)
                    for e in events:
                        e.state = state
                        e.current_event = current_event.id
                        intellect.learn(e)
                    # import pdb; pdb.set_trace()
                    intellect.reason()
                except ObjectDoesNotExist:
                    print 'state policy not found'

                try:
                    award_policy = policies.get(type=Policy.AWARD_POLICY)
                    intellect = Intellect()
                    intellect.learn(award_policy.rule)
                    intellect.learn(state)
                    intellect.reason()
                except ObjectDoesNotExist:
                    print 'award policy not found'
      
        return HttpResponse(status=200)
