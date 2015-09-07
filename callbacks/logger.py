import os
import time

from ansible import utils
from ansible.module_utils import basic
from ansible.utils.unicode import to_unicode, to_bytes

from tasks.models import TaskLog, TaskExecution


class CallbackModule(object):
    def __init__(self):
        self.disabled = False
        self.printed_playbook = False
        self.playbook = None
        self.playbook_name = None
        self.inventory = None
        self.log_message = ''
        self.log_type = 'info'

    def append_to_log(self, msg):
        self.log_message += msg+"\n"

    def flush_to_database(self, has_errors=False):
        self.log_type = 'info'

        if has_errors:
            self.log_type = 'error'

        taskexecution_id = self.inventory.get_group('tasker').get_variables().get('taskexecution_id')

        tasklog = TaskLog(taskexecution=TaskExecution.objects.get(pk=taskexecution_id), log=self.log_message)
        tasklog.save()

    def runner_on_failed(self, host, res, ignore_errors=False):
        results2 = res.copy()
        results2.pop('invocation', None)

        item = results2.get('item', None)

        if item:
            msg = "failed: [%s] => (item=%s) => %s" % (host, item, utils.jsonify(results2))
        else:
            msg = "failed: [%s] => %s" % (host, utils.jsonify(results2))

        self.append_to_log(msg)

    def runner_on_ok(self, host, res):
        results2 = res.copy()
        results2.pop('invocation', None)

        item = results2.get('item', None)

        changed = results2.get('changed', False)
        ok_or_changed = 'ok'
        if changed:
            ok_or_changed = 'changed'

        msg = "%s: [%s] => (item=%s)" % (ok_or_changed, host, item)

        self.append_to_log(msg)

    def runner_on_skipped(self, host, item=None):
        if item:
            msg = "skipping: [%s] => (item=%s)" % (host, item)
        else:
            msg = "skipping: [%s]" % host

        self.append_to_log(msg)

    def runner_on_unreachable(self, host, res):
        item = None

        if type(res) == dict:
            item = res.get('item', None)
            if isinstance(item, unicode):
                item = utils.unicode.to_bytes(item)
            results = basic.json_dict_unicode_to_bytes(res)
        else:
            results = utils.unicode.to_bytes(res)
        host = utils.unicode.to_bytes(host)
        if item:
            msg = "fatal: [%s] => (item=%s) => %s" % (host, item, results)
        else:
            msg = "fatal: [%s] => %s" % (host, results)

        self.append_to_log(msg)

    def runner_on_no_hosts(self):
        self.append_to_log("FATAL: no hosts matched or all hosts have already failed -- aborting")
        pass

    def playbook_on_task_start(self, name, is_conditional):
        name = utils.unicode.to_bytes(name)
        msg = "TASK: [%s]" % name
        if is_conditional:
            msg = "NOTIFIED: [%s]" % name

        self.append_to_log(msg)

    def playbook_on_setup(self):
        self.append_to_log('GATHERING FACTS')
        pass

    def playbook_on_play_start(self, name):
        self.playbook = self.play.playbook
        self.inventory = self.playbook.inventory

        self.append_to_log("PLAY [%s]" % name)
        pass

    def playbook_on_stats(self, stats):
        """Complete: Flush log to database"""
        has_errors = False
        hosts = stats.processed.keys()

        for h in hosts:
            t = stats.summarize(h)

            if t['failures'] > 0 or t['unreachable'] > 0:
                has_errors = True

            msg = "Host: %s, ok: %d, failures: %d, unreachable: %d, changed: %d, skipped: %d" % (h, t['ok'], t['failures'], t['unreachable'], t['changed'], t['skipped'])
            self.append_to_log(msg)

        self.flush_to_database(has_errors)
