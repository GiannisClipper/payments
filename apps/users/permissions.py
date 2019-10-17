from rest_framework import permissions


class IsAdminUserOrOwner(permissions.BasePermission):
    '''Permits admins or owners to access users objects.'''

    message = 'No permission to access data.'

    def has_object_permission(self, request, view, obj):

        if request.method == 'POST':
            return False

        return request.user.is_staff or request.user == obj
