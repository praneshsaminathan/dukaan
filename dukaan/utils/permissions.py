from rest_framework import permissions


class IsProductOwnerOrReadOnly(permissions.BasePermission):
    """
    permission to only allow admin or superuser of the project to edit it.
    Assumes the user model instance has an `role` and 'is_superuser' attribute.
    """

    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        elif request.user and request.user.is_authenticated:
            return bool(
                request.user.source.id == 'ffe2a59a-56ed-4364-80ac-12f8d1fa44ed' and
                (request.user.role.name in ['Owner', 'Administrator'] or request.user.is_superuser)
            )

        return False


class IsBuyer(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return bool(request.user.role.name in ['Buyer'])


class IsSeller(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return bool(request.user.role.name in ['Seller'])


class IsSelfOrIsOwnerOrIsAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            user = obj.created_by
            return bool(
                user == request.user or request.user.role.name in ['Owner', 'Administrator'])

