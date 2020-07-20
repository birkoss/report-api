from rest_framework import status, authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ProjectReadSerializer, ProjectWriteSerializer
from ..models import Project


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
        print(request.data)
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
