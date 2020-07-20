from django.conf.urls import include
from django.urls import path

from . import views as api_views


urlpatterns = [
    path(
        'admin/auth/oauth/',
        include('rest_framework_social_oauth2.urls')
    ),
    path(
        'social/login/',
        api_views.SocialLogin.as_view(),
        name="api-social-login"
    ),
    path(
        'status',
        api_views.UserStatus.as_view(),
        name='api-status'
    ),
]
