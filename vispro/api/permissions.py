from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.http import JsonResponse

# You can apply role checks globally with middleware or decorators.
def admin_only(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            return JsonResponse({'error': 'Admin access only'}, status=403)
        return view_func(request, *args, **kwargs)
    return wrapper

class IsOwnerOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

class RoleBasedPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        # Anonymous users are denied
        if not user or not user.is_authenticated:
            return False

        # Admin → full access
        if user.is_superuser or user.is_staff:
            return True

        # Managers (in group "Managers") → read and write
        if user.groups.filter(name='Managers').exists():
            return True

        # Normal users → read-only
        if request.method in SAFE_METHODS:
            return True

        return False
