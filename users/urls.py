from django.urls import path

from users.api.views import SocialLoginView


urlpatterns = [
    path('oauth/login/', SocialLoginView.as_view())
]
