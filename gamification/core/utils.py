# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

from models import Points, Project, ProjectBadge
from gamification.badges.models import ProjectBadgeToUser

def badge_count(user):
    """
    Given a user or queryset of users, this returns the badge
    count at each badge level that the user(s) have earned.

    Example:

     >>> badge_count(User.objects.filter(username='admin'))
     [{'count': 0, 'badge__level': '1'}, {'count': 0, 'badge__level': '2'}, {'count': 0, 'badge__level': '3'}, {'count': 0, 'badge__level': '4'}]

    Uses a single database query.
    """

    projects = Project.objects.all().values('id','name','description')
    projects = list(projects)

    projectbadges = ProjectBadge.objects.all()
    points = Points.objects.filter(user=user)

    for project in projects:
        badges = projectbadges.filter(project_id=project['id']).values('id','name')
        badges = list(badges)

        for badge in badges:
            badge_points = points.filter(projectbadge_id=badge['id'])
            total = badge_points.aggregate(models.Sum('value'))
            badge_points = badge_points.values('value','date_awarded','description')
            badge_points = list(badge_points)
            badge['awarded'] = badge_points
            badge['total'] = total['value__sum']

        project['badges'] = badges

    return projects


def top_n_points_winners(projects, n):
    """
    Given a particular project, this returns the top n points
    winners at each badge level.

    Example:

     >>> top_five_badge_winners(Project.objects.filter(projectname='geoq'))
     [{'count': 0, 'badge__level': '1'}, {'count': 0, 'badge__level': '2'}, {'count': 0, 'badge__level': '3'}, {'count': 0, 'badge__level': '4'}]

    """
    points = Points.objects.all()
    projects = projects.values('id','active','description','private')
    projects = list(projects)

    for project in projects:
        projectbadges = ProjectBadge.objects.filter(project_id=project['id']).values('id','description')
        projectbadges = list(projectbadges)

        for badge in projectbadges:
            badge_points_winners = points.filter(projectbadge_id=badge['id']).select_related('user__username').values('user_id','user__username').annotate(points_count=models.Sum('value')).order_by('-points_count')[:n]
            badge['winners'] = badge_points_winners

        project['badges'] = projectbadges

    return projects

def project_badge_awards(project):
    """
    Given a particular project, this returns all badge winners.
    """
    ids = ProjectBadge.objects.filter(project=project).values('id')

    user_badges = ProjectBadgeToUser.objects.filter(projectbadge__in=ids)\
        .values('user__username', 'projectbadge__name', 'created', 'projectbadge__badge__icon', 'projectbadge__awardLevel', 'projectbadge__tags')

    project_teams = project[0].teams.all()

    from collections import defaultdict
    groups = defaultdict(list)
    scores = defaultdict(int)
    teams = defaultdict(str)
    for obj in user_badges:
        username = obj['user__username']
        groups[username].append({
            'badge':str(obj['projectbadge__name']),
            'date':str(obj['created']),
            'icon':str(obj['projectbadge__badge__icon']),
            'tags':str(obj['projectbadge__tags']),
            'points':str(obj['projectbadge__awardLevel'])})

        #Find any teams the user is on that are on this project
        user_team = ''
        for project_team in project_teams:
            if username in [(u.username) for u in project_team.members.all()]:
                user_team = str(project_team.name)
        teams[username] = user_team

        scores[username] += obj['projectbadge__awardLevel']

    #add scores
    items = groups.items()
    for i in range(len(items)):
        items[i] = items[i] + (scores[items[i][0]],) + (teams[items[i][0]],)

    return sorted(items, key=lambda rec: rec[2],reverse=True)

def get_files_in_dir(mypath):
    from os import listdir
    from os.path import isfile, join
    return [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]


def top_n_badge_winners(project, num=3):
    """
    Given a particular project, this returns the top n badge
    winners at each badge level.

    Example:

     >>> top_n_badge_winners(Project.objects.filter(name='geoq'),5)
    """
    projectbadges = ProjectBadge.objects.filter(project=project)
    ids = projectbadges.values('id')
    badges = projectbadges.values('id','name','description','badge__icon','awardLevel')

    pbtu = ProjectBadgeToUser.objects.filter(projectbadge__in=ids)
    badges = list(badges)

    for badge in badges:
        badge['leaders'] = top_n_badge_project_winners(pbtu,badge['id'],num)
        del badge['id']

    return badges

def top_n_project_badge_winners(project,badge,num):
    """
    Given a particular project and badge, determine top n leaders
    """

    pbtu = ProjectBadgeToUser.objects.filter(projectbadge=badge)
    badge.leaders = top_n_badge_project_winners(pbtu, badge.id, num)

    return badge

def top_n_badge_project_winners(pbtu_qs,pb_id,num):
    topn = pbtu_qs.filter(projectbadge__id=pb_id).values('user__username').annotate(awarded=models.Count('user__username')).order_by('-awarded')[:num]
    return list(topn)

def users_project_points(user,project):
    """
    Find out a user's total points won on project, factoring in weighted values of badges
    """
    total = ProjectBadge.objects.filter(user=user,project=project).aggregate(models.Sum('awardLevel'))
    return total['awardLevel__sum']

def users_total_points(user):
    """
    Find out a user's points from all projects
    """
    total = ProjectBadge.objects.filter(user=user).aggregate(models.Sum('awardLevel'))
    return total['awardLevel__sum']

def user_project_badge_count(user,project):
    """
    Given a user or queryset of users, this returns the badge
    count at each badge level that the user(s) have earned.

    Example:

     >>> badge_count(User.objects.filter(username='admin'))
     [{'count': 0, 'badge__level': '1'}, {'count': 0, 'badge__level': '2'}, {'count': 0, 'badge__level': '3'}, {'count': 0, 'badge__level': '4'}]

    Uses a single database query.
    """

    projectbadges = ProjectBadge.objects.filter(project_id=project.id).values('id','name','description')
    projectbadgeids = projectbadges.values('id')
    points = Points.objects.filter(user=user,projectbadge__id__in=projectbadgeids)
    badges = list(projectbadges)

    for badge in badges:
        badge_points = points.filter(projectbadge_id=badge['id'])
        total = badge_points.aggregate(models.Sum('value'))
        badge_points = badge_points.values('value','date_awarded','description')
        badge_points = list(badge_points)
        badge['awarded'] = badge_points
        badge['total'] = total['value__sum']

    return badges