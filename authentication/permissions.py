# permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrManager(BasePermission):
    """
    Managers can view all, but edit only their own.
    Normal users can only access their own.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True  # admins can do everything

        if request.method in SAFE_METHODS:
        # Managers can view all, users only their own
            return request.user.role == 'manager' or obj.owner == request.user


        # Only owners can edit or delete
        return obj.owner == request.user
