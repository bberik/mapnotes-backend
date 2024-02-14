from rest_framework.routers import DefaultRouter
from .views import WorkspaceViewSet, NodeViewSet, EdgeViewSet, upload_image
from django.urls import include, path


router = DefaultRouter()
router.register(r'workspaces', WorkspaceViewSet)
router.register(r'nodes', NodeViewSet)
router.register(r'edges', EdgeViewSet)

urlpatterns = [
    # API Endpoints
    path("api/resources/", include(router.urls)),
    path("api/uploadimage", upload_image)
]
