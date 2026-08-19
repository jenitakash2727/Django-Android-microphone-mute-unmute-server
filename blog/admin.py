from django.contrib import admin

from .models import MicrophoneCommand


@admin.register(MicrophoneCommand)
class MicrophoneCommandAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "command",
        "status",
        "result",
        "created_at",
        "executed_at",
    )

    list_filter = (
        "command",
        "status",
    )

    search_fields = (
        "command",
        "result",
    )

    ordering = (
        "-created_at",
    )