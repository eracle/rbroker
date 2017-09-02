from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from core.models import Device


class OwnerPermissions(IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class DeviceOwnerPermissions(OwnerPermissions):

    def has_object_permission(self, request, view, obj):
        if not super().has_object_permission(request, view, obj):
            return False

        device = get_object_or_404(Device, pk=request.data['device'])
        return device.customer == request.user
