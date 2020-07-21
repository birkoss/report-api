from django.db import models
from django.template.defaultfilters import slugify

from core.models import TimeStampedModel, UUIDModel
from users.models import User


class Project(UUIDModel, TimeStampedModel):
    name = models.CharField(max_length=100, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Log(UUIDModel, TimeStampedModel):
    name = models.CharField(max_length=100, null=False, blank=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='logs')

    def __str__(self):
        return self.name


class EntryLevel(models.Model):
    slug = models.SlugField(max_length=100, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(EntryLevel, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.name)
            self.save()


class Entry(UUIDModel, TimeStampedModel):
    log = models.ForeignKey(Log, on_delete=models.CASCADE)
    level = models.ForeignKey(EntryLevel, on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.log.name + " (" + self.date_added + ")"
