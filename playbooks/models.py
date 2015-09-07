from django.db import models


class Playbook(models.Model):
    name = models.CharField(max_length=48)
    repo = models.CharField(max_length=256)
    playbook = models.CharField(max_length=48)

    def __unicode__(self):
        return self.name
