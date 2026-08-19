
import os
import subprocess
import tempfile

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


SEVEN_ZIP = r"C:\Program Files\7-Zip\7z.exe"


@csrf_exempt
def verify_zip_password(request):

    # ==========================================
    # METHOD CHECK
    # ==========================================

    if request.method != "POST":

        return JsonResponse(
            {
                "success": False,
                "message": "Only POST request is allowed."
            },
            status=405
        )

    # ==========================================
    # ZIP FILE
    # ==========================================

    zip_file = request.FILES.get("zip_file")

    if not zip_file:

        return JsonResponse(
            {
                "success": False,
                "message": "ZIP file is required."
            },
            status=400
        )

    # ==========================================
    # PASSWORD
    # ==========================================

    password = request.POST.get("password", "")

    if not password:

        return JsonResponse(
            {
                "success": False,
                "message": "Password is required."
            },
            status=400
        )

    # ==========================================
    # CHECK 7-ZIP
    # ==========================================

    if not os.path.isfile(SEVEN_ZIP):

        return JsonResponse(
            {
                "success": False,
                "message": "7-Zip is not installed on the server."
            },
            status=500
        )

    # ==========================================
    # TEMP DIRECTORY
    # ==========================================

    temp_dir = os.path.join(
        settings.MEDIA_ROOT,
        "zip_temp"
    )

    os.makedirs(
        temp_dir,
        exist_ok=True
    )

    # Random temporary filename
    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".zip",
        dir=temp_dir
    )

    zip_path = temp_file.name

    # ==========================================
    # SAVE ZIP
    # ==========================================

    try:

        with temp_file:

            for chunk in zip_file.chunks():

                temp_file.write(chunk)

    except Exception as e:

        if os.path.exists(zip_path):
            os.remove(zip_path)

        return JsonResponse(
            {
                "success": False,
                "message": f"Upload failed: {str(e)}"
            },
            status=500
        )

    # ==========================================
    # VERIFY PASSWORD WITH 7-ZIP
    # ==========================================

    try:

        command = [
            SEVEN_ZIP,
            "t",
            zip_path,
            f"-p{password}",
            "-y"
        ]

        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=60,
            creationflags=subprocess.CREATE_NO_WINDOW
        )

        # ======================================
        # PASSWORD CORRECT
        # ======================================

        if result.returncode == 0:

            return JsonResponse(
                {
                    "success": True,
                    "message": "Password is correct."
                }
            )

        # ======================================
        # PASSWORD WRONG
        # ======================================

        return JsonResponse(
            {
                "success": False,
                "message": "Incorrect password."
            }
        )

    except subprocess.TimeoutExpired:

        return JsonResponse(
            {
                "success": False,
                "message": "ZIP verification timed out."
            },
            status=408
        )

    except Exception as e:

        return JsonResponse(
            {
                "success": False,
                "message": f"Verification error: {str(e)}"
            },
            status=500
        )

    finally:

        # ======================================
        # DELETE TEMP ZIP
        # ======================================

        if os.path.exists(zip_path):

            try:
                os.remove(zip_path)

            except OSError:
                pass