from rest_framework.viewsets import ModelViewSet
from core.utils.response import success_response

class BaseViewSet(ModelViewSet):

    def list(self,request,*args,**kwargs):
        response =super().list(request,*args,**kwargs)
        return success_response(response.data)
    
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return success_response(response.data)
    
    def create(self,request,*args,**kwargs):
        response =super().create(request,*args,**kwargs)
        return success_response(response.data,message="Created Successfully")
    
    def update(self,request,*args,**kwargs):
        response = super().update(request,*args,**kwargs)
        return success_response(response.data,message="Updated successfully")
    
    def partial_update(self, request, *args, **kwargs):
        response =super().partial_update(request, *args, **kwargs)
        return success_response(response.data,message="Updated successfully")
    
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return success_response(message="Deleted successfully")