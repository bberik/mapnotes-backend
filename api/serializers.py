from rest_framework import serializers
from .models.app import Workspace, Node, Edge
from .models import CustomUser



class EdgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Edge
        fields = '__all__'

class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = '__all__'


class WorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = '__all__'


class WorkspaceDetailedSerializer(serializers.ModelSerializer):
    nodes = NodeSerializer(many=True, read_only=True, source='workspace_nodes')
    edges = EdgeSerializer(many=True, read_only=True, source='workspace_edges')
    
    class Meta:
        model = Workspace
        fields = (
            "id",
            "created_at",
            "updated_at",
            "title",
            "nodes",
            "edges",
            # "blocks"
        )
        
