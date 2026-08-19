from django.urls import path

from .Microphone import (
    microphone_command,
    get_microphone_command,
    command_done,
)


urlpatterns = [

    # Android → Django
    path(
        "api/microphone/command/",
        microphone_command,
        name="microphone_command",
    ),

    # Windows Client → Django
    path(
        "api/microphone/command/get/",
        get_microphone_command,
        name="get_microphone_command",
    ),

    # Windows Client → Mark completed
    path(
        "api/microphone/command/<int:command_id>/done/",
        command_done,
        name="command_done",
    ),

]