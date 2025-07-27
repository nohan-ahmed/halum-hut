from rest_framework import permissions
from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Allows access only to the owner of the object, for all HTTP methods.
    """

    def has_permission(self, request, view):
        # Allow access only if user is authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Allow access only if the user is the owner of the object
        return hasattr(obj, 'user') and obj.user == request.user


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit or delete it.
    """

    def has_permission(self, request, view):
        # Allow read-only permissions for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Otherwise, ensure the user is authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the owner of the post
        return obj.user == request.user
    
    
class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to edit or delete objects.
    """
    
    def has_permission(self, request, view):
        # Allow read-only permissions for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Otherwise, ensure the user is an admin
        return request.user and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to admins
        return request.user and request.user.is_staff

