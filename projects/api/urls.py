from django.urls import path

from . import views as api_views


urlpatterns = [
    path(
        'projects',
        api_views.Projects.as_view(),
        name='api-projects'
    ),
    path(
        'projects/<str:project_id>',
        api_views.ProjectsDetails.as_view(),
        name='api-projects-details'
    ),
]
