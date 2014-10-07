# -*- coding: utf-8 -*-

from django.contrib import admin
from django import forms
from django.contrib.auth.models import User

from models import Badge,BadgeSettings, ProjectBadge, ProjectBadgeToUser
from singleton_models.admin import SingletonModelAdmin

class BadgeAdmin(admin.ModelAdmin):
    fields = ('name','level','icon',)
    list_display = ('name','level')
    
    
class ProjectBadgeAdmin(admin.ModelAdmin):
    list_display = ('name','description','awardLevel')
    fields = ('name','description','project','badge','awardLevel','multipleAwards','tags')

class BadgeSettingsAdmin(admin.ModelAdmin):
    fields = ('awardLevel','multipleAwards')
    list_display = ('awardLevel','multipleAwards')

class ProjectBadgeToUserAdminForm(forms.ModelForm):
    class Meta:
        model = ProjectBadgeToUser

    def __init__(self, *args, **kwargs):
        super(ProjectBadgeToUserAdminForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.order_by('username')

class ProjectBadgeToUserAdmin(admin.ModelAdmin):
    list_display = ('projectbadge','user','created')
    form = ProjectBadgeToUserAdminForm

admin.site.register(Badge, BadgeAdmin)
#admin.site.register(BadgeSettings, BadgeSettingsAdmin)
admin.site.register(ProjectBadge, ProjectBadgeAdmin)
admin.site.register(ProjectBadgeToUser, ProjectBadgeToUserAdmin)
