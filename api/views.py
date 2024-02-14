from rest_framework import viewsets
from .models.app import Workspace, Node, Edge
from .serializers import (
    WorkspaceSerializer,
    NodeSerializer,
    EdgeSerializer,
    WorkspaceDetailedSerializer
)
from django.db.models import Q
from .permissions import (
    CreateWorkspacePermission,
    ListWorkspacePermission,
    RetrieveUpdateDeleteWorkspacePermission,
    CreateNodeEdgePermission,
    RetrieveUpdateDeleteNodeEdgePermission
)

from rest_framework.decorators import api_view
from rest_framework.response import Response
import boto3
import app.settings as settings


class WorkspaceViewSet(viewsets.ModelViewSet):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [CreateWorkspacePermission]
        elif self.action == 'list':
            permission_classes = [ListWorkspacePermission]
        else:
            permission_classes = [RetrieveUpdateDeleteWorkspacePermission]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        if (self.request.user.is_authenticated):
            serializer.save(creator=self.request.user)
        else:
            serializer.save(creator=None)
        return super().perform_create(serializer)

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            if self.action == "list":
                return None
            elif self.action in [
                "destroy",
                "update",
                "retrieve",
                "partial_update"
            ]:
                return Workspace.objects.filter(creator=None)
        else:
            if self.action == "list":
                return Workspace.objects.filter(creator=user)
            else:
                return Workspace.objects.filter(
                    Q(creator=user) | Q(creator=None)
                )

    def get_serializer_class(self):
        if self.action == "retrieve":
            return WorkspaceDetailedSerializer
        return super().get_serializer_class()


class NodeViewSet(viewsets.ModelViewSet):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [CreateNodeEdgePermission]
        else:
            permission_classes = [RetrieveUpdateDeleteNodeEdgePermission]
        return [permission() for permission in permission_classes]


class EdgeViewSet(viewsets.ModelViewSet):
    queryset = Edge.objects.all()
    serializer_class = EdgeSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [CreateNodeEdgePermission]
        else:
            permission_classes = [RetrieveUpdateDeleteNodeEdgePermission]
        return [permission() for permission in permission_classes]


@api_view(['POST'])
def upload_image(request):
    # Get the uploaded image file
    uploaded_image = request.FILES.get('image')

    # Upload the image to AWS S3
    s3_client = boto3.client('s3')
    file_path = f'uploads/{uploaded_image.name}'
    s3_client.upload_fileobj(
        uploaded_image,
        settings.AWS_STORAGE_BUCKET_NAME,
        file_path
    )

    # Generate the URL for the uploaded image
    s3_url = \
        f'https://{settings.AWS_STORAGE_BUCKET_NAME}.\
        s3.amazonaws.com/{file_path}'

    return Response({
        "success": 1,
        "file": {
            "url": s3_url,
        }
    })
