from django.core.exceptions import ValidationError

from .models import Folder, Project


def get_folder(**kwargs):
    kwargs['is_active'] = True

    folder = None

    try:
        folder = Folder.objects.filter(**kwargs).first()
    except ValidationError:
        pass

    return folder


def get_project(**kwargs):
    kwargs['is_active'] = True

    project = None

    try:
        project = Project.objects.filter(**kwargs).first()
    except ValidationError:
        pass

    return project
