from django.db import models
from django.template.defaultfilters import slugify

from core.models import TimeStampedModel, UUIDModel
from users.models import User


class Project(UUIDModel, TimeStampedModel):
    name = models.CharField(max_length=100, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Folder(UUIDModel, TimeStampedModel):
    name = models.CharField(max_length=100, null=False, blank=False)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='folders'
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class LogLevel(models.Model):
    slug = models.SlugField(max_length=100, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(LogLevel, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.name)
            self.save()


class Log(UUIDModel, TimeStampedModel):
    folder = models.ForeignKey(
        Folder, on_delete=models.CASCADE, related_name="logs"
    )
    level = models.ForeignKey(LogLevel, on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.folder.name  # + " (" + self.date_added + ")"
