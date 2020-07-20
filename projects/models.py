from django.db import models

from core.models import TimeStampedModel, UUIDModel
from users.models import User


class Project(UUIDModel, TimeStampedModel):
    name = models.CharField(max_length=100, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
