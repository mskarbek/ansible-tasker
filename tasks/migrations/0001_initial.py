# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_fsm
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('playbooks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=48)),
                ('enabled', django_fsm.FSMField(default=b'true', max_length=50)),
                ('playbook', models.ForeignKey(to='playbooks.Playbook')),
            ],
        ),
        migrations.CreateModel(
            name='TaskExecution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True, editable=False)),
                ('started', models.DateTimeField(null=True, blank=True)),
                ('ended', models.DateTimeField(null=True, blank=True)),
                ('state', django_fsm.FSMField(default=b'new', max_length=50)),
                ('task', models.ForeignKey(to='tasks.Task')),
            ],
        ),
        migrations.CreateModel(
            name='TaskLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log', models.TextField()),
                ('taskexecution', models.ForeignKey(to='tasks.TaskExecution')),
            ],
        ),
    ]
