from django import template
from django.utils.text import slugify

register = template.Library()

@register.filter('teamify')
def teamify(nodes):
    team_members = {}

    for team in nodes:
        team_members[str(slugify(team.name))] = []
        for member in team.memberpoints['members']:
            team_members[str(slugify(team.name))].append(member);

    return team_members

