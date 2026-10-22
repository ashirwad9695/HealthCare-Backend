from rest_framework import permissions

class IsPatientOwnerOrStaff(permissions.BasePermission):
    """
    Object-level permission to only allow owners of a patient record or staff to view/edit it.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.created_by == request.user
