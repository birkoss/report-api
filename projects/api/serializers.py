from rest_framework import serializers

from users.api.serializers import UserSerializer

from ..models import Project, Folder


class ProjectReadSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'user', 'date_added']


class ProjectWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['name']


class FolderReadSerializer(serializers.ModelSerializer):
    project = ProjectReadSerializer(read_only=True)

    class Meta:
        model = Folder
        fields = ['id', 'name', 'project', 'date_added']


class FolderWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ['name']
