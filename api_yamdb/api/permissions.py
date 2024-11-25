from rest_framework import permissions


class IsAuthorModeratorAdminOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        """Разрешение на уровне объекта."""
        return (
            request.method in permissions.SAFE_METHODS
            or request.user == obj.author
            or request.user.is_moderator
            or request.user.is_admin
        )


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        """Разрешение на уровне запроса для админа."""
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated
            and (request.user.is_admin or request.user.is_superuser)
        )
