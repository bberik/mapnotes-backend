from django.db import models
import uuid
from django_editorjs import EditorJsField


from app.settings import AUTH_USER_MODEL


class TagChoices(models.TextChoices):
    H1 = 'h1', 'Heading 1'
    H2 = 'h2', 'Heading 2'
    H3 = 'h3', 'Heading 3'
    H4 = 'h4', 'Heading 4'
    H5 = 'h5', 'Heading 5'
    H6 = 'h6', 'Heading 6'
    P = 'p', 'Paragraph'
    IMG = 'img', 'Image'


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Workspace(BaseModel):
    title = models.CharField(max_length=255, null=True, default=None)
    creator = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, null=True
    )


class Node(BaseModel):
    title = models.CharField(max_length=255,
                             null=True,
                             default=None,
                             blank=True
                             )
    x = models.IntegerField()
    y = models.IntegerField()
    workspace = models.ForeignKey(Workspace,
                                  on_delete=models.CASCADE,
                                  related_name="workspace_nodes"
                                  )
    is_expanded = models.BooleanField(default=True)
    body = EditorJsField(
        editorjs_config={
            "tools": {
                "Image": {
                    "config": {
                        "endpoints": {
                            "byFile": '/uploadi/'
                        },
                    }
                },
            }
        },
        null=True,
        blank=True,
        default=None
    )


class Edge(BaseModel):
    source = models.ForeignKey(
        Node,
        on_delete=models.CASCADE,
        related_name='source'
    )
    target = models.ForeignKey(
        Node,
        on_delete=models.CASCADE,
        related_name='target'
    )
    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name="workspace_edges"
    )
