from rest_framework import permissions

class HasPermission(permissions.BasePermission):
    """
    Custom permission to check if user's role has the required permission.
    Since DRF expects classes in `permission_classes`, we use a factory pattern
    or override `get_permissions` in the ViewSet.
    """
    required_permission = None

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Super admin check (Optional: if we want to hardcode a super admin role)
        # But we rely on the Role's permission list.
        
        if not self.required_permission:
            return True
            
        role = request.user.role
        if not role:
            return False
            
        return self.required_permission in role.permissions

def require_permission(perm_name):
    """
    Factory function to create a permission class with a specific required permission.
    Example usage in ViewSet:
    permission_classes = [require_permission('USERS_VIEW')]
    """
    class PermClass(HasPermission):
        required_permission = perm_name
    return PermClass
