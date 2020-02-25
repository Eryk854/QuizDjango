from rest_framework import permissions

class PermissionError(BaseException):
    pass

class MyPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action != 'list':
            if request.user.is_anonymous:
                raise PermissionError
            else:
                return request.user.is_admin

        else:
            return True

