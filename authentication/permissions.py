from rest_framework.permissions import BasePermission


class IsClientAdmin(BasePermission):
    """Custom client user permissions."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'CA'


class IsNormalUser(BasePermission):
    """Custom normal user permissions."""

    def hs_permissions(self, request, view):
        return request.is_authenticated and request.user.role == 'NU'


class IsProfileOwner(BasePermission):
    """Custom profile owner permissions."""

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user
