from rest_framework import serializers

from users.api.serializers import UserSerializer

from ..models import Log, Project


class SimpleLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = ['id', 'name']


class ProjectReadSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    logs = SimpleLogSerializer(read_only=True, many=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'user', 'date_added', "logs"]


class ProjectWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['name']


class LogReadSerializer(serializers.ModelSerializer):
    project = ProjectReadSerializer(read_only=True)

    class Meta:
        model = Log
        fields = ['id', 'name', 'project', 'date_added']


class LogWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = ['name']
