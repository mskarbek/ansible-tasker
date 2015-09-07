from __future__ import absolute_import

import os
import time
from tempfile import NamedTemporaryFile

from celery import shared_task

from .models import TaskExecution


@shared_task
def execute(taskexecution_id):
    from ansible.playbook import PlayBook
    from ansible.inventory import Inventory
    from ansible import callbacks
    from ansible import utils

    utils.VERBOSITY = 0
    playbook_cb = callbacks.PlaybookCallbacks(verbose=utils.VERBOSITY)
    stats = callbacks.AggregateStats()
    runner_cb = callbacks.PlaybookRunnerCallbacks(stats, verbose=utils.VERBOSITY)

    time.sleep(5)

    taskexecution = TaskExecution.objects.get(pk=taskexecution_id)
    taskexecution.start()
    taskexecution.save()

    inventory = "[local]\n\
localhost   ansible_connection=local\n\
\n\
[tasker]\n\
localhost\n\
\n\
[tasker:vars]\n\
taskexecution_id={}".format(taskexecution_id)

    hosts = NamedTemporaryFile(delete=False)
    hosts.write(inventory)
    hosts.close()

    pb = PlayBook(
        playbook='/tmp/main.yml',
        host_list=hosts.name,
        # remote_user='mskarbek',
        callbacks=playbook_cb,
        runner_callbacks=runner_cb,
        stats=stats,
        # private_key_file='/path/to/key.pem'
    )

    results = pb.run()

    playbook_cb.on_stats(pb.stats)

    os.remove(hosts.name)

    status = results.get('localhost')

    if status['failures'] > 0 or status['unreachable'] > 0:
        taskexecution.failed()
        taskexecution.save()
        return False

    taskexecution.succeed()
    taskexecution.save()
    return True
