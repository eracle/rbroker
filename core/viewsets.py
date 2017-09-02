from django.db import transaction
from django.shortcuts import get_object_or_404
from django_q.tasks import async
from rest_framework import mixins
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from core.models import Task, Device
from core.permissions import OwnerPermissions, DeviceOwnerPermissions
from core.serializers import TaskSerializer
from core.tasks import task_timeout


class TaskListViewSet(mixins.ListModelMixin,
                      GenericViewSet):
    serializer_class = TaskSerializer
    permission_classes = [OwnerPermissions]

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user, state=Task.AVAILABLE).all()


# Add an API method to let a Device notify the beginning of the execution of a Task
class TaskViewSet(GenericViewSet):
    serializer_class = TaskSerializer
    permission_classes = [DeviceOwnerPermissions]

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user).all()

    def begin(self, request, pk, *args, **kwargs):
        task = get_object_or_404(Task, pk=pk)

        device_pk = request.data['device']
        device = get_object_or_404(Device, pk=device_pk)

        # new_state = request.data['state']
        with transaction.atomic():
            if task.state != Task.AVAILABLE:
                raise ValidationError('Task is not available')
            task.state = Task.EXECUTING
            task.device = device
            task.save()

        async(task_timeout, task.uuid)

        return Response(data=self.get_serializer(task).data)

    # Add an API method to let a Device notify the result of an execution of a Task
    def success(self, request, pk, *args, **kwargs):

        task = get_object_or_404(Task, pk=pk)
        with transaction.atomic():
            if task.state == Task.COMPLETED:
                raise ValidationError('Task was already completed')

            if task.state != Task.EXECUTING:
                raise ValidationError('Task is not executed')

            task.state = Task.COMPLETED
            task.save()

        return Response(data={'ok'})

    def failure(self, request, pk, *args, **kwargs):
        task = get_object_or_404(Task, pk=pk)

        with transaction.atomic():
            if task.state == Task.COMPLETED:
                raise ValidationError('Task was already completed')

            if task.state != Task.EXECUTING:
                raise ValidationError('Task is not executed')

            task.state = Task.AVAILABLE
            task.device = None
            task.save()

        return Response(data={'ok'})
