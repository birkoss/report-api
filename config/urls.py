from django.contrib import admin
from django.conf.urls import include
from django.urls import path

from users.api.views import SocialLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/oauth/', include('rest_framework_social_oauth2.urls')),
    path('oauth/login/', SocialLoginView.as_view()),
]
