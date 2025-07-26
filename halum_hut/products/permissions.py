from rest_framework import permissions

class IsSellerOrReadOnly(permissions.BasePermission):
    """
    - SAFE_METHODS (GET, HEAD, OPTIONS): allowed to everyone
    - Non-safe methods (POST, PUT, PATCH, DELETE): 
        - User must be authenticated
        - User must have a seller_account
        - Object.seller must match user's seller_account (for object-level permissions)
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        # Must be authenticated and have a seller_account
        return request.user.is_authenticated and hasattr(request.user, 'seller_account')

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        # Only the seller who owns the product can modify it
        if not hasattr(request.user, 'seller_account'):
            return False

        return obj.seller == request.user.seller_account


class IsSellerOrReadOnlyForProductData(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated and hasattr(request.user, 'seller_account')
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        seller = getattr(request.user, 'seller_account', None)
        return seller and getattr(obj.product, 'seller', None) == seller

