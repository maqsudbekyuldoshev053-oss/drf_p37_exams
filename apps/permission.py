
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrAdminReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff or request.user.is_superuser:
            return True
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or request.user.is_superuser:
            return True
        if request.method in SAFE_METHODS:
            return True
        if request.user.method == "DELETE":
            return True
        return obj.author == request.user
