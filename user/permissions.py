from rest_framework import permissions

from .models import User


class IsPageOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS and \
                (not obj.is_private or request.user in obj.followers.all()):
            return True

        return (request.user.is_authenticated and
                obj.owner == request.user)


class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.role == User.Roles.USER
                     or request.user.role == User.Roles.MODERATOR
                     or request.user.role == User.Roles.ADMIN))

    def has_object_permission(self, request, view, obj):
        return (request.user.is_authenticated
                and (request.user.role == User.Roles.USER
                     or request.user.role == User.Roles.MODERATOR
                     or request.user.role == User.Roles.ADMIN)
                and obj.user == request.user)


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.role == User.Roles.MODERATOR
                     or request.user.role == User.Roles.ADMIN))

    def has_object_permission(self, request, view, obj):
        return (request.user.is_authenticated
                and (request.user.role == User.Roles.MODERATOR
                     or request.user.role == User.Roles.ADMIN)
                )


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.role == User.Roles.ADMIN)

    def has_object_permission(self, request, view, obj):
        return (request.user.is_authenticated
                and request.user.role == User.Roles.ADMIN)
