from rest_framework import permissions

class IsAdminOrReadonly(permissions.IsAdminUser):
    
    def has_permission(self, request, view):
        admin_permission = super().has_permission(request, view)
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return admin_permission
        
        
class IsReviewUserOrAdminOrReadOnly(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.author == request.user or request.user.is_staff