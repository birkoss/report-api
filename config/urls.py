from django.contrib import admin
from django.conf.urls import include
from django.urls import path

from users.api.urls import urlpatterns as users_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
] + users_urlpatterns
