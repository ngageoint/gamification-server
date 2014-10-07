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


from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView, ListView

from django.contrib import admin
admin.autodiscover()
from gamification.core.models import Project
from gamification.core.views import *
from gamification.events.views import handle_event, assign_badge

urlpatterns = patterns("",
    url(r"^gamification/$", TemplateView.as_view(template_name="core/index.html"), name="home"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^account/", include("account.urls")),
    url(r"^users/?$", UserView.as_view(template_name='core/users.html'), name='user_list'),
    url(r"^users/(?P<username>[\w.@]+)/", include("gamification.core.urls")),
    url(r"^projects/$", master_project_list),

    url(r"^projects/all/", MasterProjectListView.as_view(template_name='core/masterprojects_list.html'), name='master-project-list'),
    url(r"^projects/(?P<projectname>[\w ]+)/?$", ProjectListView.as_view(template_name='core/projects_list.html'), name='project-list'),
    url(r"^projects/(?P<projectname>[\w ]+)/admin/?$", ProjectAdminListView.as_view(template_name='core/project_admin.html'), name='project-admin'),

    url(r"^projects/(?P<projectname>[\w ]+)/(?P<phrase>\w+)/?$", ProjectListView.as_view(template_name='core/projects_list.html'), name='project-list'),

    url(r"^projects/(?P<projectname>[\w ]+)/leaders/?$", project_all_badgeleaders_view),
    # url(r"^projects/(?P<projectname>\w+)/badges/?$", BadgeListView.as_view(template_name='core/badge_list.html'), name='badge-list'),
    url(r"^projects/(?P<projectname>[\w ]+)/badges/(?P<badgename>\w+)/leaders/?$", project_badgeleaders_view),
    url(r'^badges/?$', MasterBadgeListView.as_view(template_name='core/master_badge_list.html'), name='master-badge-list'),
    url(r'^users/(?P<username>[\w.@]+)/projects/(?P<projectname>[\w ]+)/event/?$', handle_event),
    url(r'^users/(?P<username>[\w.@]+)/assign_badge/(?P<badge>[\w ]+)?$', assign_badge),
    url(r'^users/(?P<username>[\w.@]+)/create/?$', create_new_user),
    url(r'^$', MasterBadgeListView.as_view(template_name="core/index.html"), name="home"),
    url(r'^users/(?P<username>[\w .-@])/projects/(?P<projectname>\w+)/event/?$', handle_event),
    url(r'^users/(?P<username>[\w .-@])/assign_badge/(?P<badge>\w+)?$', assign_badge),
    url(r'^users/(?P<username>[\w .-@])/create/?$', create_new_user),
    url(r'^$', TemplateView.as_view(template_name="core/index.html"), name="home"),

    # Open Badges interoperability. Define an Issuer
    url(r'^projects/(?P<projectname>\w+)/badges/(?P<badgename>\w+)/issuer/?$', \
        get_issuer, name="openbadges_issuer"),

    # and a way to retrieve a badge's image
    url(r'^projects/(?P<projectname>\w+)/badges/(?P<badgename>\w+)/image/?$', \
        get_image, name="openbadges_image"),

    # a badge's metadata
    url(r'^projects/(?P<projectname>\w+)/badges/(?P<badgename>\w+)/metadata/?$', \
        get_metadata, name="openbadges_metadata"),
        
    # a badge's criteria
    url(r'projects/(?P<projectname>\w+)/badges/(?P<badgename>\w+)/criteria/?$', \
        get_criteria, name='openbadges_criteria'),
        
    # badge instance metadata
    url(r'projects/(?P<projectname>\w+)/badges/(?P<badgename>\w+)/users/(?P<username>[\w .-@])/award/?$', \
        get_badge_award, name='openbadges_award'),
)

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
