from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.role =='admin')
    
class IsEmployer(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and hasattr(request.user,'employer'))
    
class IsCandidate(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and hasattr(request.user, 'candidate'))
    
class IsEmployerOrAdmin(BasePermission):
    def has_permission(self,request,view): 

        if not request.user.is_authenticated:
            return False

        return (hasattr(request.user,'employer')or request.user.role =='admin')   