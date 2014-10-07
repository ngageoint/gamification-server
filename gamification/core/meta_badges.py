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


from gamification.core.models import Points
from gamification.badges import MetaBadge

class Gold(MetaBadge):
    id = 1
    name = "Gold"
    model = Points
    one_time_only = False
    title = "Gold Award"
    level = "1"
    def check_project(self,instance):
        return False


class Silver(MetaBadge):
    id = 2    
    name = "Silver"
    model = Points
    one_time_only = False
    title = "Silver Award"
    level = "2"

    def check_project(self, instance):
        return False


class Bronze(MetaBadge):
    id = 3    
    name = "Bronze"
    model = Points
    one_time_only = False
    title = "Bronze Award"
    level = "3"

    def check_project(self, instance):
        return False
