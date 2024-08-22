from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):        
        # if request.method == 'GET': #* With this implementation, 'Head' & 'Option' requires user to be an admin & we don't want that.
        #* Better approach would be to use 'Safe_Methods'
        if request.method in SAFE_METHODS:
            return True
        
        return bool(request.user and request.user.is_staff)
    

class ViewCustomerHistoryPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('store.view_history')