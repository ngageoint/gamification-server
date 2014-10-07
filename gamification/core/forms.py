# This technical data was produced for the U. S. Government under Contract No. W15P7T-13-C-F600, and
# is subject to the Rights in Technical Data-Noncommercial Items clause at DFARS 252.227-7013 (FEB 2012)

from django import forms
from django.contrib.auth.models import User
from gamification.badges.models import ProjectBadge

class AwardForm(forms.Form):

    award_id = forms.ModelChoiceField(label=(u'Award'),
                                        queryset=ProjectBadge.objects.all(),
                                        required=True)
    points = forms.ChoiceField(label=(u'Points to Award'),
                               widget=forms.Select(),
                               choices=([('1','1'),('5','5'),('10','10'),('20','20'),('50','50'),]),
                               required=True)
    comment = forms.CharField(label=(u'Comment'),
                              max_length=255)