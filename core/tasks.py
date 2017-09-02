
from django.db import transaction

from core.models import Task

import time

from rbroker.settings import TASK_EXECUTION_TIME


def task_timeout(task_uuid):

    print('Waiting %s sec before timeout' % TASK_EXECUTION_TIME)
    time.sleep(TASK_EXECUTION_TIME)

    print('Getting task, uuid: %s' % task_uuid)
    with transaction.atomic():
        task = Task.objects.get(uuid=task_uuid)
        if task.state == Task.EXECUTING:
            print('Time out, task: %s' % task)

            task.state = Task.AVAILABLE
            task.device = None
            task.save()
        else:
            print('Task not executing anymore')
