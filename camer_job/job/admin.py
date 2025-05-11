from django.contrib import admin

from .models import Task, Domain

admin.site.register(Domain)
admin.site.register(Task)
