# -*- coding: utf-8 -*-

from gamification.core.models import Points
from gamification.badges.utils import MetaBadge
from gamification.badges.models import ProjectBadge

def check_points(self,instance):
    return False

def create_badge_classes():
    pbadges = ProjectBadge.objects.all()

    for pbadge in pbadges:
        cls = type(pbadge.name.encode('ascii','ignore'),(MetaBadge,),{'id':badge.id,'name':badge.name,'model':Points,'level':badge.level,'check_points':check_points})

# create_badge_classes()


