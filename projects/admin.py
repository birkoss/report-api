from django.contrib import admin

from .models import Project, Log, LogLevel, Folder

admin.site.register(Project)
admin.site.register(Log)
admin.site.register(Folder)
admin.site.register(LogLevel)
