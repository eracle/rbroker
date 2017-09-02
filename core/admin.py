from django.contrib import admin

from core.models import Device, Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    pass


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    pass
