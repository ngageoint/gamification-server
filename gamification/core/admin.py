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

import reversion
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms
from models import Project, UserProfile, Points, Team
from django.contrib import admin

class ObjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')

class UserProfileAdmin(ObjectAdmin):
    list_display = ('user','score')

class PointAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_awarded', 'projectbadge', 'value')

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'date_created')
    filter_horizontal = ('members',)

class ProjectAdmin(admin.ModelAdmin):
    model = Project
    list_filter = ("private", "active", "visual_theme")
    filter_horizontal = ('supervisors', 'teams',)

    normal_fields = ('name', 'private', 'active',  'description', 'visual_theme', 'project_closing_date')
    readonly_fields = ('created_at', 'updated_at')

    save_on_top = True
    save_as = True

    advanced_fields = ( 'viewing_pass_phrase', 'supervisors', 'teams', 'background_image', 'properties' )
    desc = 'The settings below are advanced.  Please contact and admin if you have questions.'

    fieldsets = (
        (None, {'fields': normal_fields}),
        ('Advanced Settings', {'classes': ('collapse',),
                               'description': desc,
                               'fields': advanced_fields,
                               }))



admin.site.register(Project, ProjectAdmin)
#admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Points, PointAdmin)
admin.site.register(Team, TeamAdmin)