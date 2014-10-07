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


from django.contrib.auth.models import User
from django.views.generic import ListView
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.conf import settings
from django.utils.datastructures import SortedDict
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from models import Project, Points
from gamification.badges.models import ProjectBadge, ProjectBadgeToUser
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
import json
from gamification.badges.utils import project_badge_count
from gamification.core.utils import badge_count,top_n_badge_winners,user_project_badge_count, top_n_project_badge_winners,\
project_badge_awards, users_project_points, get_files_in_dir

from gamification.core.models import Project
from gamification.core.forms import AwardForm
from gamification.core.serializers import ProjectSerializer, PointsSerializer
from rest_framework import renderers
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
import mimetypes


class PointsListView(ListView):

    paginate_by = 15
    model = Points

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs['username'])
        return Points.objects.filter(user=user)

    def get_context_data(self, **kwargs):
        cv = super(PointsListView, self).get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs['username'])
        cv['profile'] = badge_count(user)
        return cv

class MasterProjectListView(ListView):

    paginate_by = 15
    model = Project

    def get_queryset(self):
        return Project.objects.all()

    def get_context_data(self, **kwargs):
        cv = super(MasterProjectListView, self).get_context_data(**kwargs)
        cv['profile'] = top_n_badge_winners(cv['object_list'],5)
        return cv

class UserProjectPointsView(ListView):
    paginate_by = 15
    model = User

    def get_queryset(self):
        return User.objects.filter(username=self.kwargs['username'])

    def get_context_data(self, **kwargs):
        cv = super(UserProjectPointsView, self).get_context_data(**kwargs)
        project = get_object_or_404(Project, name=self.kwargs['projectname'])
        user = cv['object_list'][0]

        cv['username'] = user.username
        cv['projectbadges'] = user_project_badge_count(user,project)
        cv['projectname'] = project.description
        return cv

class ProjectListView(ListView):

    paginate_by = 15
    model = Project

    def get_queryset(self):
        return Project.objects.filter(name=self.kwargs['projectname'])

    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)

        try:
            phrase = self.kwargs['phrase']
        except:
            phrase = ""

        projects = context['object_list']
        context['top_n_badges'] = top_n_badge_winners(projects,5)
        context['badge_awards'] = project_badge_awards(projects)
        context['badge_awards_json'] = json.dumps(context['badge_awards'])
        context['project'] = projects[0]
        context['properties_json'] = json.dumps(projects[0].properties or {})

        context['code'] = phrase
        if projects[0].visual_theme:
            try:
                files = get_files_in_dir("gamification/static/themes/" + projects[0].visual_theme)
                js_files = [ f for f in files if f.endswith(".js") ]

                context['theme_files'] = json.dumps(js_files, ensure_ascii=False)
                context['theme_files_js'] = [ f for f in files if f.endswith(".js") ]
                context['theme_files_css'] = [ f for f in files if f.endswith(".css") ]
            except Exception, e:
                context['theme_files_error'] = str(e)

        context['admin'] = self.request.user.is_superuser or self.request.user.groups.filter(name='admin_group').count() > 0
        return context


class ProjectAdminListView(ListView):

    model = Project

    def get_queryset(self):
        return Project.objects.filter(name=self.kwargs['projectname'])

    def get_context_data(self, **kwargs):
        context = super(ProjectAdminListView, self).get_context_data(**kwargs)

        project = context['object_list'][0]

        context['project'] = project
        context['all_users'] = User.objects.all().order_by('username')
        context['badges'] = ProjectBadge.objects.filter(project=project)
        context['admin'] = self.request.user.is_superuser or \
                           self.request.user.groups.filter(name='admin_group').count() > 0 or \
                           self.request.user in project.supervisors.all()

        return context


class BadgeListView(ListView):

    model = ProjectBadge

    def get_queryset(self):
        project = get_object_or_404(Project, name=self.kwargs['projectname'])
        return ProjectBadge.objects.filter(project=project).values('name','description','awardLevel','multipleAwards','badge__icon')

    def get_context_data(self, **kwargs):
        cv = super(BadgeListView, self).get_context_data(**kwargs)
        cv['project_name'] = self.kwargs['projectname']
        return cv

class MasterBadgeListView(ListView):

    model = ProjectBadge

    def get_queryset(self):
        return ProjectBadge.objects.filter(project__private=False).values('name','description','created','awardLevel','multipleAwards','tags','badge__icon','project__name','project__description').order_by('project__name','-awardLevel','name')

    def get_context_data(self, **kwargs):
        cv = super(MasterBadgeListView, self).get_context_data(**kwargs)
        return cv

class UserView(ListView):

    model = User

    def get_queryset(self):
        return User.objects.all().order_by('last_name')

    def get_context_data(self, **kwargs):
        cv = super(UserView, self).get_context_data(**kwargs)
        return cv


def award(request, *args, **kwargs):
    if request.method == 'POST':
        form = AwardForm(request.POST)
        if form.is_valid():
            user = get_object_or_404(User, username=kwargs['username'])
            projectbadge = ProjectBadge.objects.get(pk=request.POST['award_id'])
            points = Points(user=user,projectbadge=projectbadge,value=request.POST['points'],description=request.POST['comment'])
            points.save()
            return HttpResponseRedirect('/users/%s/projects/%s/badges' % (kwargs['username'], kwargs['projectname']))

    else:
        form = AwardForm()

    return render(request, 'core/award.html', { 'form': form, })

# REST interface

def projects(request, *args, **kwargs):
    if request.method == 'GET':
        try:
            user = get_object_or_404(User,username=kwargs['username'])
            project = get_object_or_404(Project,name=kwargs['projectname'])
        except Http404, e:
            context = { 'message' : e.__str__().split()[1] + ' not found' }
            return HttpResponse(json.dumps(context),'application/json',404)

        projbadges = ProjectBadge.objects.filter(project=project)
        badge_info = project_badge_count(user,project,projbadges)
        badge_detail_list = []
        for bi in badge_info:
            bstr = '{ "name":"%s", "awarded":%d, "url":"%s"}' % \
               ( bi['projectbadge__name'], bi['count'], bi['projectbadge__badge__icon'])
            badge_detail_list.append(json.loads(bstr))

        resp = '{"username":"%s", "badges":%s}' % (user.username, json.dumps(badge_detail_list))
        return HttpResponse(resp, mimetype="application/json")
    elif request.method == 'PUT':
        point_args = {}
        if request.GET.__contains__('comment'):
            point_args['description'] = request.GET['comment']

        if request.GET.__contains__('points'):
            point_args['value'] = int(request.GET['points'])
        else:
            context = {'message' : 'No points included in request'}
            return HttpResponse(json.dumps(context), 'application/json', 400)

        try:
            point_args['user'] = get_object_or_404(User,username=kwargs['username'])
            project = get_object_or_404(Project,name=kwargs['projectname'])
        except Http404, e:
            context = { 'message' : e.__str__().split()[1] + ' not found' }
            return HttpResponse(json.dumps(context),'application/json',404)
            
        award = request.GET['award']

        try:
            point_args['projectbadge'] = get_object_or_404(ProjectBadge,name=award)
        except Http404, e:
            context = { 'message' : 'Project not found' }
            return HttpResponse(json.dumps(context), 'application/json', 404)

        # award points
        points = Points(**point_args)
        points.save()

        return HttpResponseRedirect('/users/%s/projects/%s' % (point_args['user'], project))

@api_view(('GET',))
@renderer_classes((renderers.TemplateHTMLRenderer,renderers.JSONRenderer))
def master_project_list(request):
    queryset = Project.objects.filter(private=False)

    if request.accepted_renderer.format == 'html':
        actives = []
        non_actives = []
        for project in queryset:
            if project.active:
                actives.append(project)
            else:
                non_actives.append(project)

        data = {'active_projects': actives,
                'non_active_projects': non_actives}
        return Response(data, template_name='core/projects.html')

    # JSONRenderer
    serializer = ProjectSerializer(instance=queryset)
    data = serializer.data
    return Response(data)


@api_view(('GET',))
@renderer_classes((renderers.TemplateHTMLRenderer,renderers.JSONRenderer))
def user_points_list(request,username):
    user = get_object_or_404(User, username=username)
    queryset = badge_count(user)

    if request.accepted_renderer.format == 'html':
        data = {'profile': queryset, 'username': user.username}
        return Response(data, template_name='core/points_list.html')

    #JSON Renderer
    return Response(queryset)

@api_view(('GET',))
def user_points(request,username,projectname):
    user = get_object_or_404(User, username=username)
    project = get_object_or_404(Project, name=projectname)
    points = users_project_points(user,project)
    data =  {'user':user.username, 'project':project.name, 'points':points}

    return Response(data)


@api_view(('GET',))
@renderer_classes((renderers.TemplateHTMLRenderer,renderers.JSONRenderer))
def user_project_points_list(request,username,projectname,rendertype='html'):
    user = get_object_or_404(User, username=username)
    project = get_object_or_404(Project, name=projectname)
    totals = user_project_badge_count(user,project)

    rendertype = rendertype or request.accepted_renderer.format
    if rendertype == 'html':
        data = {'projectbadges': totals, 'username': user.username, 'projectname':project.description}
        return Response(data, template_name='core/user_project_points_list.html')

    #JSON Renderer
    return Response(totals)

@api_view(('GET',))
@renderer_classes((renderers.TemplateHTMLRenderer,renderers.JSONRenderer))
def user_project_badges_list(request,username,projectname,rendertype='html'):
    user = get_object_or_404(User, username=username)

    project_names = projectname.split(',')
    projects = Project.objects.filter(name__in=project_names)

    total_points = 0
    badges = []
    tags = {}
    for project in projects:

        #Find all badges from the project
        projbadges = ProjectBadge.objects.filter(project=project).order_by('badge__level')
        prefix = 'https://' if request.is_secure() else 'http://'
        url = prefix + request.get_host() + settings.STATIC_URL

        #TODO: Find list of points for Leaderboard
        #Get list of badges user has
        badges = badges + project_badge_count(user,project,projbadges,url)

        for pb in projbadges:
            tag_list = pb.tags
            if tag_list:
                tag_list = tag_list.lower().split(",")
                for tag in tag_list:
                    tag = tag.strip()
                if tags.has_key(tag):
                    tags[tag] += 1
                else:
                    tags[tag] = 1

        #Count all the values of user's points
        pbtu = ProjectBadgeToUser.objects.filter(user__username=username,projectbadge__project=project)
        for userbadge in pbtu:
            total_points += userbadge.projectbadge.awardLevel

    rendertype = rendertype or request.accepted_renderer.format
    if rendertype == 'html':
        data = {'profile': badges, 'points':total_points, 'tags':tags}
        return Response(data, template_name='core/badge_list.html')

    #JSON
    badge_detail_list = []

    for bi in badges:
        bstr = '{ "name":"%s", "awarded":%d, "url":"%s" }' % \
            ( bi['projectbadge__name'], bi['count'], bi['projectbadge__badge__icon'])
        badge_detail_list.append(json.loads(bstr))

    return Response(badge_detail_list)


@api_view(('GET',))
@renderer_classes((renderers.TemplateHTMLRenderer,renderers.JSONRenderer))
def project_all_badgeleaders_view(request,projectname):
    project = get_object_or_404(Project, name=projectname)

    try:
        count = int(request.QUERY_PARAMS['count'])
    except Exception:
        count = 10

    project_leaders = top_n_badge_winners(project,count)

    if request.accepted_renderer.format == 'html':
        return Response(data, template_name='core/user_project_points_list.html')

    #JSON Renderer
    return Response(project_leaders)

@api_view(('GET',))
@renderer_classes((renderers.TemplateHTMLRenderer,renderers.JSONRenderer))
def project_badgeleaders_view(request,projectname,badgename):
    project = get_object_or_404(Project, name=projectname)
    badge = get_object_or_404(ProjectBadge, name=badgename)

    try:
        count = int(request.QUERY_PARAMS['count'])
    except Exception:
        count = 10

    badge_leaders = top_n_project_badge_winners(project,badge,count)
    d = SortedDict()
    d["name"] = badge_leaders.name
    d["description"] = badge_leaders.description
    d["leaders"] = badge_leaders.leaders

    if request.accepted_renderer.format == 'html':
        return Response(data, template_name='core/user_project_points_list.html')

    #JSON Renderer

    return Response(d)

@api_view(('POST',))
def create_new_user(request, *args, **kwargs):
    username = kwargs['username'].lower()
    ucount = User.objects.filter(username=username).count()
    if ucount > 0:
        return HttpResponse("User already exists", 400)

    user = User.objects.create_user(username=username)
    user.save()
    return HttpResponse("User Created")
    
@api_view(('GET',))
@renderer_classes((renderers.JSONRenderer,))
def get_issuer(request, projectname, badgename):
    project = get_object_or_404(Project, name=projectname)
    d = SortedDict()
    d['name'] = project.description
    d['url'] = project.url
    
    return Response(d)
    
    
@api_view(('GET',))
def get_image(request, projectname, badgename):
    project = get_object_or_404(Project, name=projectname)
    projbadge = get_object_or_404(ProjectBadge, name=badgename)
    mimetype = mimetypes.guess_type(projbadge.badge.icon.path)
    
    return HttpResponse(projbadge.badge.icon.read(), mimetype=mimetype)
    
@api_view(('GET',))
@renderer_classes((renderers.JSONRenderer,))
def get_metadata(request, projectname, badgename):
    project = get_object_or_404(Project, name=projectname)
    projbadge = get_object_or_404(ProjectBadge, name=badgename, project=project)
    d = SortedDict()
    d['name'] = projbadge.name
    d['description'] = projbadge.description
    d['image'] = request.build_absolute_uri(reverse('openbadges_image', kwargs={'projectname':projectname, \
        'badgename':badgename}))
    d['criteria'] = 'criteria'
    d['issuer'] = request.build_absolute_uri(reverse('openbadges_issuer', kwargs={'projectname':projectname, \
        'badgename':badgename}))
    
    return Response(d)
    
class PlainTextRenderer(renderers.BaseRenderer):
    media_type = 'text/plain'
    format = 'txt'
    
    def render(self, data, media_type=None, renderer_context=None):
        return data.encode(self.charset)
        
    
@api_view(('GET',))
@renderer_classes((PlainTextRenderer,))
def get_criteria(request, projectname, badgename):
    project = get_object_or_404(Project, name=projectname)
    projbadge = get_object_or_404(ProjectBadge, name=badgename, project=project)    
    
    return Response(projbadge.description)
    
@api_view(('GET',))
@renderer_classes((renderers.JSONRenderer,))
def get_badge_award(request, projectname, badgename, username):
    project = get_object_or_404(Project, name=projectname)
    projbadge = get_object_or_404(ProjectBadge, name=badgename, project=project)
    user = get_object_or_404(User, username=username)
    
    try:
        pbtu = ProjectBadgeToUser.objects.filter(projectbadge=projbadge,user=user).latest('created')
    except ObjectDoesNotExist:
        return HttpResponse("Award not found for that user", 404)

    d = SortedDict()
    d['uid'] = "%d#%d" % (projbadge.id,pbtu.id)
    r = {}
    r['type'] = "email"
    r['hashed'] = False
    r['identity'] = user.email
    d['recipient'] = r

    d['issuedOn'] = pbtu.created
    d['badge'] = request.build_absolute_uri(reverse('openbadges_metadata', kwargs={'projectname':projectname, \
        'badgename':badgename }))
    v = {}
    v['type'] = "hosted"
    v['url'] = request.build_absolute_uri(request.get_full_path())
    d['verify'] = v
    
    return Response(d)
    



       
