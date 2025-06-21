from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrManager(BasePermission):
    """
    Admins can do everything.
    Managers can view everything, but edit/delete only their own.
    Users can only access their own data.
    """
    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.role == 'admin':
            return True

        if request.method in SAFE_METHODS:
            return user.role == 'manager' or obj.owner == user

        # Only owners can edit/delete
        return obj.owner == user
