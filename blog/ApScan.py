from django.http import JsonResponse
from rest_framework.decorators import api_view
from scapy.all import ARP, Ether, srp


@api_view(["POST"])
def lookup_mac(request):

    target_ip = request.data.get("ip")

    print("Received IP:", target_ip)

    if not target_ip:
        return JsonResponse({
            "success": False,
            "error": "IP is required"
        }, status=400)

    try:
        packet = (
            Ether(dst="ff:ff:ff:ff:ff:ff")
            / ARP(pdst=target_ip)
        )

        result = srp(
            packet,
            timeout=5,
            verbose=0
        )[0]

        print("ARP responses:", len(result))

        if not result:
            return JsonResponse({
                "success": False,
                "ip": target_ip,
                "error": "No device responded"
            }, status=404)

        sent, received = result[0]

        print("Found IP:", received.psrc)
        print("Found MAC:", received.hwsrc)

        return JsonResponse({
            "success": True,
            "ip": received.psrc,
            "mac": received.hwsrc
        })

    except Exception as e:
        print("ARP ERROR:", e)

        return JsonResponse({
            "success": False,
            "error": str(e)
        }, status=500)