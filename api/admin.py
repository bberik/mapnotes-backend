from django.contrib import admin

from .models.app import (
    Node,
    Edge,
    Workspace,
)

# Register your models here.

admin.site.register(Node)
admin.site.register(Edge)
admin.site.register(Workspace)
