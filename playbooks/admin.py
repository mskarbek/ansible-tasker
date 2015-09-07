from django.contrib import admin

from .models import Playbook


@admin.register(Playbook)
class PlaybookAdmin(admin.ModelAdmin):
    fields = ['name', 'repo', 'playbook']
    list_display = ['name', 'repo', 'playbook']
