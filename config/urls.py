from django.contrib import admin
from django.conf.urls import include
from django.urls import path

from projects.api.urls import urlpatterns as projects_urlpatterns
from users.api.urls import urlpatterns as users_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
] + users_urlpatterns + projects_urlpatterns
