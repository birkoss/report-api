from django.core.exceptions import ValidationError

from .models import Log, Project


def get_log(**kwargs):
    log = None

    try:
        log = Log.objects.filter(**kwargs).first()
    except ValidationError:
        pass

    return log


def get_project(**kwargs):
    project = None

    try:
        project = Project.objects.filter(**kwargs).first()
    except ValidationError:
        pass

    return project
