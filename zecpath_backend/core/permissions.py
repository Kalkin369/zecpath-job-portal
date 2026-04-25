from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role =='is_staff'
    
class IsEmployer(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user,'employer')
    
class IsCandidate(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'candidate')