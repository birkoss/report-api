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
            id=project_id
        )

        folders = Folder.objects.filter(
            project=project,
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
                'folder': FolderReadSerializer(instance=folder, many=False).data,
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

    def delete(self, request, category_id, format=None):
        category = TransactionCategory.objects.filter(
            id=category_id, user=request.user
        ).annotate(transactions=Count('transaction')).first()

        if category is None:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "message": "This is not a valid category"
            }, status.HTTP_404_NOT_FOUND)

        if category.transactions == 0:
            category.delete()
        else:
            category.is_active = False
            category.save()

        return Response({
            "status": status.HTTP_200_OK
        })


class Projects(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        projects = Project.objects.filter(
            user=request.user
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
                'project': ProjectReadSerializer(instance=project, many=False).data,
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

    def delete(self, request, category_id, format=None):
        category = TransactionCategory.objects.filter(
            id=category_id, user=request.user
        ).annotate(transactions=Count('transaction')).first()

        if category is None:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "message": "This is not a valid category"
            }, status.HTTP_404_NOT_FOUND)

        if category.transactions == 0:
            category.delete()
        else:
            category.is_active = False
            category.save()

        return Response({
            "status": status.HTTP_200_OK
        })
