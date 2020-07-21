from .models import Project


def get_project(**kwargs):
    project = None

    try:
        project = Project.objects.filter(**kwargs).first()
    except ValidationError:
        pass

    return project
