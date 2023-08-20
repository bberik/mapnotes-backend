from rest_framework import viewsets
from .models.app import Workspace, Node, Edge
from .serializers import WorkspaceSerializer, NodeSerializer, EdgeSerializer, WorkspaceDetailedSerializer
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated


class WorkspaceViewSet(viewsets.ModelViewSet):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
        return super().perform_create(serializer)
    
    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            if self.action == "list":
                return None
            elif self.action in ["destroy", "update", "retrieve"]:
                return Workspace.objects.filter(creator=None)
        else:
            if self.action == "list":
                return Workspace.objects.filter(creator=user)
            else:
                return Workspace.objects.filter(Q(creator=user) | Q(creator=None))
    
    
    def get_serializer_class(self):
        if self.action == "retrieve": 
            return WorkspaceDetailedSerializer
        return super().get_serializer_class()

class NodeViewSet(viewsets.ModelViewSet):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer


class EdgeViewSet(viewsets.ModelViewSet):
    queryset = Edge.objects.all()
    serializer_class = EdgeSerializer


