import logging
import requests
import ipaddress
from typing import Any, Dict
from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from .models import Visitor

logger = logging.getLogger(__name__)

# Create your views here.
def get_client_ip(request):
    # https://stackoverflow.com/a/4581997
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def get_address_info(address: str) -> Dict[str, Any]:
    is_private = ipaddress.ip_address(address).is_private
    if is_private:
        # address is private - just return false - no lookup
        return {"success": False}
    try:
        r = requests.get(
            f"https://ipapi.co/{address}/json/",
            headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36"
            },
        )
        r.raise_for_status()
        response_body = r.json()
    except:
        # request raised an exception
        logger.info("Unable to resolve address information")
        return {"success": False}

    response_body["success"] = True
    return response_body


def is_safe_address(address: str, key: str) -> bool:
    try:
        response = requests.get(
            f"http://v2.api.iphub.info/ip/{address}", headers={"X-Key": key}
        )
        block = response.json()["block"]
    except:
        logger.info("Unable to resolve address type")
        block = 1  # default to an unsafe address
    return block == 0


def index(request):
    ip = get_client_ip(request)
    info = get_address_info(ip)
    address_safe = is_safe_address(address, settings.VPN_KEY)
    city_region = f'{info.get("city", "Unknown")}, {info.get("region", "Unknown")}'

    try:
        visitor_obj = Visitor.objects.get(visitor_ip=ip)
        visitor_obj.time_visited = timezone.now()
    except Visitor.DoesNotExist:
        visitor_obj = Visitor(
            visitor_ip=ip,
            time_visited=timezone.now(),
            visitor_city_region=city_region,
            is_safe=address_safe,
        )
    visitor_obj.save()
    return render(
        request,
        "zweedendev/index.html",
        {"visitor_ip": visitor_obj.visitor_ip, "server_time": timezone.now()},
    )
