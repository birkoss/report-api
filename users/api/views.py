from django.contrib.auth import login, authenticate
from django.http import JsonResponse

from rest_framework import authentication, generics, permissions, status, views
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from requests.exceptions import HTTPError
 
from social_django.utils import load_strategy, load_backend
from social_core.backends.oauth import BaseOAuth2
from social_core.exceptions import MissingBackend, AuthTokenError, AuthForbidden

from . import serializers


class UserStatus(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        serializer = serializers.UserSerializer(instance=request.user)

        return Response({
            'account': serializer.data,
            'status': status.HTTP_400_BAD_REQUEST,
        })


class SocialLogin(generics.GenericAPIView):
    """Log in using facebook"""
    serializer_class = serializers.SocialSerializer
    permission_classes = [permissions.AllowAny]
 
    def post(self, request):
        """Authenticate user through the provider and access_token"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        provider = serializer.data.get('provider', None)
        strategy = load_strategy(request)

        print(request)

        try:
            backend = load_backend(
                strategy=strategy, name=provider, redirect_uri=None
            )
        except MissingBackend:
            return Response({
                'error': 'Please provide a valid provider',
                'status': status.HTTP_400_BAD_REQUEST,
            }, status=status.HTTP_400_BAD_REQUEST)

        print(backend)

        try:
            if isinstance(backend, BaseOAuth2):
                access_token = serializer.data.get('access_token')
            user = backend.do_auth(access_token)

        except HTTPError as error:
            return Response({
                "error": {
                    "access_token": "Invalid token",
                    "details": str(error)
                },
                'status': status.HTTP_400_BAD_REQUEST,
            }, status=status.HTTP_400_BAD_REQUEST)
        except AuthTokenError as error:
            return Response({
                "error": "Invalid credentials",
                "details": str(error),
                'status': status.HTTP_400_BAD_REQUEST,
            }, status=status.HTTP_400_BAD_REQUEST)

        print(user.email)
        print(user.id)

        try:
            authenticated_user = backend.do_auth(access_token, user=user)

        except HTTPError as error:
            return Response({
                "error": "invalid token",
                "details": str(error),
                'status': status.HTTP_400_BAD_REQUEST,
            }, status=status.HTTP_400_BAD_REQUEST)

        except AuthForbidden as error:
            return Response({
                "error": "invalid token",
                "details": str(error),
                'status': status.HTTP_400_BAD_REQUEST,
            }, status=status.HTTP_400_BAD_REQUEST)

        if authenticated_user and authenticated_user.is_active:
            login(request, authenticated_user)

            token = Token.objects.get(user=user)

            #customize the response to your needs
            response = {
                "email": authenticated_user.email,
                "token": token.key,
                'status': status.HTTP_200_OK,
            }
            return Response(status=status.HTTP_200_OK, data=response)
