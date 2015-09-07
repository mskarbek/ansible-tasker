from django.contrib import admin

from fsm_admin.mixins import FSMTransitionMixin

from .models import Task, TaskExecution, TaskLog


class TaskExecutionInline(admin.TabularInline):
    model = TaskExecution
    extra = 0
    readonly_fields = ['uuid', 'task', 'started', 'ended', 'state']


@admin.register(Task)
class TaskAdmin(FSMTransitionMixin, admin.ModelAdmin):
    readonly_fields = ['enabled']
    fields = ['name', 'playbook', 'enabled']
    fsm_field = ['enabled']
    list_display = ['name', 'playbook', 'enabled']
    inlines = [TaskExecutionInline]


@admin.register(TaskExecution)
class TaskExecutionAdmin(FSMTransitionMixin, admin.ModelAdmin):
    readonly_fields = ['uuid', 'started', 'ended', 'state']
    fields = ['uuid', 'task', 'started', 'ended', 'state']
    fsm_field = ['state']
    list_display = ['uuid', 'task', 'started', 'ended', 'state']


@admin.register(TaskLog)
class TaskLogAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'taskexecution']
    fields = ['id', 'taskexecution', 'log']
    list_display = ['id', 'taskexecution']
