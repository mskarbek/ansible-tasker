import uuid

from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from django_fsm import FSMField, transition

from playbooks.models import Playbook


class Task(models.Model):
    name = models.CharField(max_length=48)
    playbook = models.ForeignKey(Playbook)
    enabled = FSMField(default='true')

    def __unicode__(self):
        return self.name

    def is_enabled(self):
        if self.enabled == 'true':
            return True
        return False

    @transition(field=enabled, source='true', target='false')
    def disable(self):
        pass

    @transition(field=enabled, source='false', target='true')
    def enable(self):
        pass


class TaskExecution(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    task = models.ForeignKey(Task)
    started = models.DateTimeField(blank=True, null=True)
    ended = models.DateTimeField(blank=True, null=True)
    state = FSMField(default='new')

    def __unicode__(self):
        return str(self.uuid)

    def clean(self, *args, **kwargs):
        if not self.task.is_enabled():
            raise ValidationError(
                "Can't add new execution when task is disabled"
            )
        super(TaskExecution, self).clean(*args, **kwargs)

    @transition(field=state, source='new', target='started')
    def start(self):
        # pass
        self.started = timezone.now()
        self.save()

    @transition(field=state, source='started', target='succeed')
    def succeed(self):
        self.ended = timezone.now()
        self.save()

    @transition(field=state, source='started', target='failed')
    def failed(self):
        self.ended = timezone.now()
        self.save()


class TaskLog(models.Model):
    taskexecution = models.ForeignKey(TaskExecution)
    log = models.TextField()

    def __unicode__(self):
        return "{} - log".format(str(self.taskexecution))

from .tasks import execute


@receiver(post_save, sender=TaskExecution)
def run(sender, instance, created, **kwargs):
    if created:
        execute.delay(instance.id)
