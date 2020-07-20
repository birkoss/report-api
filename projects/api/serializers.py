from rest_framework import serializers

from users.api.serializers import UserSerializer

from ..models import Project


class ProjectReadSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'user', 'date_added']


class ProjectWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['name']
