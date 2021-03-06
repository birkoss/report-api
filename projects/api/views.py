from django.db.models import Count
from django.core.exceptions import ValidationError
from rest_framework import status, authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (FolderReadSerializer, FolderWriteSerializer,
                          ProjectReadSerializer, ProjectWriteSerializer)
from ..models import Folder, Project
from ..helpers import get_folder, get_project


class Folders(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, project_id, format=None):
        project = get_project(
            user=request.user,
            id=project_id,
        )

        folders = Folder.objects.filter(
            project=project,
            is_active=True
        ).order_by("name")

        serializer = FolderReadSerializer(instance=folders, many=True)

        return Response({
            'status': status.HTTP_200_OK,
            'folders': serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request, project_id, format=None):
        project = get_project(
            user=request.user,
            id=project_id
        )

        if project is None:
            return Response({
                'status': status.HTTP_404_NOT_FOUND,
                'message': "This is not a valid project"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = FolderWriteSerializer(data=request.data)

        if serializer.is_valid():
            folder = serializer.save(project=project)

            return Response({
                'folder': FolderReadSerializer(
                    instance=folder, many=False
                ).data,
                'status': status.HTTP_200_OK,
            })
        else:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                'message': serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)


class FoldersDetails(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, folder_id, format=None):
        folder = get_folder(
            id=folder_id
        )
        if folder is None:
            return Response({
                'status': status.HTTP_404_NOT_FOUND,
                'message': "This is not a valid folder"
            }, status=status.HTTP_404_NOT_FOUND)

        project = get_project(
            user=request.user,
            id=folder.project.id
        )
        if project is None:
            return Response({
                'status': status.HTTP_404_NOT_FOUND,
                'message': "This is not a valid folder from your account"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = FolderReadSerializer(instance=folder, many=False)

        return Response({
            'status': status.HTTP_200_OK,
            'folder': serializer.data
        }, status=status.HTTP_200_OK)

    def put(self, request, folder_id, format=None):
        folder = get_folder(
            id=folder_id,
        )

        if folder is None:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "message": "This is not a valid folder"
            }, status.HTTP_404_NOT_FOUND)

        project = get_project(
            user=request.user,
            id=folder.project.id
        )

        if project is None:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "message": "This is not a valid project"
            }, status.HTTP_404_NOT_FOUND)

        serializer = FolderWriteSerializer(folder, data=request.data)

        if serializer.is_valid():
            folder = serializer.save()

            return Response({
                'folder': FolderReadSerializer(
                    instance=folder, many=False
                ).data,
                'status': status.HTTP_200_OK,
            })
        else:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                'message': serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, folder_id, format=None):
        # @TODO : Should be in the helpers
        folder = Folder.objects.filter(
            id=folder_id,
        ).annotate(total_logs=Count('logs')).first()

        if folder is None:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "message": "This is not a valid folder"
            }, status.HTTP_404_NOT_FOUND)

        project = get_project(
            user=request.user,
            id=folder.project.id
        )
        if project is None:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "message": "This is not a valid project"
            }, status.HTTP_404_NOT_FOUND)

        if folder.total_logs == 0:
            folder.delete()
        else:
            folder.is_active = False
            folder.save()

        return Response({
            "status": status.HTTP_200_OK
        })


class Projects(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        projects = Project.objects.filter(
            user=request.user,
            is_active=True
        ).order_by("name")

        serializer = ProjectReadSerializer(instance=projects, many=True)

        return Response({
            'status': status.HTTP_200_OK,
            'projects': serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = ProjectWriteSerializer(data=request.data)

        if serializer.is_valid():
            project = serializer.save(user=request.user)

            return Response({
                'project': ProjectReadSerializer(
                    instance=project, many=False
                ).data,
                'status': status.HTTP_200_OK,
            })
        else:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                'message': serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)


class ProjectsDetails(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, project_id, format=None):
        project = get_project(
            user=request.user,
            id=project_id
        )

        if project is None:
            return Response({
                'status': status.HTTP_404_NOT_FOUND,
                'message': "This is not a valid project"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = ProjectReadSerializer(instance=project, many=False)

        return Response({
            'status': status.HTTP_200_OK,
            'project': serializer.data
        }, status=status.HTTP_200_OK)

    def put(self, request, project_id, format=None):
        project = get_project(
            id=project_id,
            user=request.user
        )

        if project is None:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "message": "This is not a valid project"
            }, status.HTTP_404_NOT_FOUND)

        serializer = ProjectWriteSerializer(project, data=request.data)

        if serializer.is_valid():
            project = serializer.save()

            return Response({
                'project': ProjectReadSerializer(
                    instance=project, many=False
                ).data,
                'status': status.HTTP_200_OK,
            })
        else:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                'message': serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, project_id, format=None):
        # @TODO : Should be in the helpers
        project = Project.objects.filter(
            id=project_id,
            user=request.user
        ).annotate(total_folders=Count('folders')).first()

        if project is None:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "message": "This is not a valid project"
            }, status.HTTP_404_NOT_FOUND)

        if project.total_folders == 0:
            project.delete()
        else:
            project.is_active = False
            project.save()

        return Response({
            "status": status.HTTP_200_OK
        })
