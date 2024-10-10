from django.core.exceptions import PermissionDenied

class CheckPermissionGroupMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.groups.filter(name = '').exists():
            #return True 
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied