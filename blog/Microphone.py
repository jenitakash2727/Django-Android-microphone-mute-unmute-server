import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import MicrophoneCommand

def home(request):
    return JsonResponse({
        "status": "online",
        "message": "Omnitrix Microphone Server is running"
    })
# ==========================================
# ANDROID → DJANGO
# POST /api/microphone/command/
# ==========================================

@csrf_exempt
def microphone_command(request):

    if request.method != "POST":
        return JsonResponse(
            {"error": "POST required"},
            status=405
        )

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON"},
            status=400
        )

    command = data.get("command")

    if command not in ["mute", "unmute"]:
        return JsonResponse(
            {
                "error": "command must be mute or unmute"
            },
            status=400
        )

    new_command = MicrophoneCommand.objects.create(
        command=command,
        status="pending",
        result=""
    )

    return JsonResponse({
        "success": True,
        "command": command,
        "id": new_command.id
    })


# ==========================================
# WINDOWS CLIENT → DJANGO
# GET /api/microphone/command/get/
# ==========================================

def get_microphone_command(request):

    if request.method != "GET":
        return JsonResponse(
            {"error": "GET required"},
            status=405
        )

    command = (
        MicrophoneCommand.objects
        .filter(status="pending")
        .order_by("created_at")
        .first()
    )

    if command is None:
        return JsonResponse({
            "command": None
        })

    return JsonResponse({
        "command": command.command,
        "id": command.id
    })


# ==========================================
# WINDOWS CLIENT → MARK DONE
# POST /api/microphone/command/<id>/done/
# ==========================================

@csrf_exempt
def command_done(request, command_id):

    if request.method != "POST":
        return JsonResponse(
            {"error": "POST required"},
            status=405
        )

    try:
        command = MicrophoneCommand.objects.get(
            id=command_id
        )

    except MicrophoneCommand.DoesNotExist:
        return JsonResponse(
            {"error": "Command not found"},
            status=404
        )

    command.status = "executed"
    command.save(
        update_fields=["status"]
    )

    return JsonResponse({
        "success": True,
        "id": command.id
    })