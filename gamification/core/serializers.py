from django.forms import widgets
from rest_framework import serializers
from models import Project, Points
from django.contrib.auth.models import User


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'created_at', 'active')

class PointsSerializer(serializers.ModelSerializer):
    username = serializers.RelatedField(source='user')
    projectbadge_name = serializers.RelatedField(source='projectbadge')

    class Meta:
        model = Points
        fields = ('username', 'projectbadge_name', 'value', 'date_awarded', 'description')
