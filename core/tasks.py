
from django.db import transaction

from core.models import Task


def task_timeout(param):
    print('Time outed task', flush=True)
    with transaction.atomic():

        task = Task.objects.get(pk=param)

        if task.state == Task.EXECUTING:
            print('Time out, task: %s' % task)

            task.state = Task.AVAILABLE
            task.device = None
            task.save()
        else:
            print('Task not executing anymore')
