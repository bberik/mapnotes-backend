from rest_framework import permissions
from .models.app import Workspace

class CreateWorkspacePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return True  

class ListWorkspacePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated  

class RetrieveUpdateDeleteWorkspacePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.creator is None:
            return True  
        elif request.user.is_authenticated:
            return obj.creator == request.user  
        else:
            return False 
        

class CreateNodeEdgePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        workspace_id = request.data.get("workspace")
        
        if workspace_id is None:
            return False  
        
        try:
            workspace = Workspace.objects.get(id=workspace_id)
        except Workspace.DoesNotExist:
            return False  
        
        if workspace.creator is None:
            return True  
        elif request.user.is_authenticated:
            return workspace.creator == request.user  
        else:
            return False 

class RetrieveUpdateDeleteNodeEdgePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        workspace = obj.workspace
        
        if workspace.creator is None:
            return True 
        elif request.user.is_authenticated:
            return workspace.creator == request.user 
        else:
            return False  


