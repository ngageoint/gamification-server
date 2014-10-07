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

from datetime import datetime
from intellect.Intellect import Intellect
from state import DemoState

# Experimental class that was used for early rules engine testing purposes
class RulesEngine(object):
    
    def reason(self, policy, state):
        intellect = Intellect()
        intellect.learn(policy)
        intellect.learn(state)
        intellect.reason()
        
    def run_test(self, policy, event_dtg):
        username = 'John Doe'
        projectname = 'training'
        event_type = 'course_complete'
        event_data = {}
        event_data[event_type] = training_event_data = {}
    
        course_ids = ['008031', '008189', '008582', '009446', '013413', '013567', '016003', '016094', '017724', '020146', '023416']

        for cid in course_ids:
            print ('Adding course {0}'.format(cid))
            training_event_data[cid] = event_dtg
            
            class Object(object):
                pass
            user = Object()
            user.username = username
            project = Object()
            project.name = projectname
            
            self.reason(policy, DemoState(user, project, event_data))

if __name__ == '__main__':
    policy1 = "from state import DemoState\nrule 'Rule 1':\n\twhen:\n\t\t$state := DemoState((project.name == 'training') and ('course_complete' in event_data) and ('008031' in event_data['course_complete']) and ('008189' in event_data['course_complete']) and ('008582' in event_data['course_complete']) and ('009446' in event_data['course_complete']) and ('013413' in event_data['course_complete']) and ('013567' in event_data['course_complete']) and ('016003' in event_data['course_complete']) and ('016094' in event_data['course_complete']) and ('017724' in event_data['course_complete']) and ('020146' in event_data['course_complete']) and ('023416' in event_data['course_complete']))\n\tthen:\n\t\t$state.award($state.user, $state.project, 'Gold')\n"
    utilIntellect = Intellect()
    policy2 = utilIntellect.local_file_uri('./mandatory_training_2.policy')
    engine = RulesEngine()
    engine.run_test(policy1, '') # User should get gold
    engine.run_test(policy2, datetime.now()) # User should get gold
    engine.run_test(policy2, datetime(2015, 1, 1)) # User should get silver
    engine.run_test(policy2, datetime(2015, 2, 1)) # User should get bronze
