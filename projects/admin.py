from django.contrib import admin

from .models import Project, Entry, EntryLevel, Log

admin.site.register(Project)
admin.site.register(Entry)
admin.site.register(Log)
admin.site.register(EntryLevel)
