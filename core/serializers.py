from rest_framework import serializers

from core.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id',
                  'state',
                  'device',
                  'uuid',
                  )
        read_only_fields = ('id',
                            'state',
                            'uuid',
                            )
