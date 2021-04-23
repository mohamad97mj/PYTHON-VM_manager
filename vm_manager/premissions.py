from rest_framework import permissions
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


class MyCustomIsAuthenticated(permissions.BasePermission):
    """
    Custom permission
    """

    def has_permission(self, request, view):
        authorization_header = request.headers.get('Authorization', '')
        if not authorization_header:
            return False

        token = authorization_header.split(' ')[1]
        username = User.objects.get(id=Token.objects.get(key=token).user_id).username
        if username == 'admin':
            return True
        elif username == 'user1':
            allowed_vms = ['VM1', ]
            requested_vms = [
                request.data.get('vmName', ''),
                request.data.get('sourceVmName', ''),
                request.data.get('destVmName', '')
            ]
            for vm in requested_vms:
                if vm and vm not in allowed_vms:
                    return False
        return True
