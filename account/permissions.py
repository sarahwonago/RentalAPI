from rest_framework.permissions import BasePermission


class IsSuperAdmin(BasePermission):
    """
    Custom permission class to allow access to superadmin only.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and  request.user.role == "superadmin"

class IsLandLord(BasePermission):
    """
    Custom permission class to allow access to landlord only.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and  request.user.role == "landlord"
    
    # def has_object_permission(self, request, view, obj):
    #     return obj.landlord == request.user
    
class IsTenant(BasePermission):
    """
    Custom permission class to allow access to tenants only.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "tenant"
    
