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
from rest_framework.response import Response
from rest_framework.decorators import api_view
from zweedendev.serializers import InfoSerializer

logger = logging.getLogger(__name__)

def i_know_he_ate_a_cheese() -> str:
    # http://www.glassgiant.com/ascii/
    return """                                                                                
                                                :~~~                            
                                               :~~~~~                           
                                              :~~~~~~~~                         
                                             ,~~~~~~~~~~:                       
       ~~=~~,                                ,~~~~~~~~~~:                       
     ::~~~~~~~,                             ::~~~~,:~~~~~                       
     :~~~~~~~~~,:                           ::~~~:.:~~~=:                       
    ::~~~~~~~~~~,:,,                        ,:,...,:~~~~,                       
    :~~~~~~~~~~=,:,,                        ,:::,,:~~~=,:                       
    :~~~~~~~,:~~:::.                      :::::::::~~~:,~                       
    :~~~~~~~:,:~:::.,,,,..,,,:::~:::::::::::::::::,~~:,~                        
    :~~~~~~~~,.,.::.::::::::::::::::::::::::::::::,..~                          
    :~~~~~~~~~:,,::,,:::::::::::::::::::::..,::::::,~                           
    ::~~~~~~~~~=::::,:::::::::::,..,:::::,::,,:::::,:                           
     ,~~~~~~~~~~,:::,,:::::::::,,:::::::::::::::::::,                           
     ,::~~~~~~~::::::,::::::::,,::::::::::::::::::::,,                          
      :,:~~~~~:,:::::,,:::::::,::::::::::::::::::::::,                          
        :,,,,,,,:::::,,:::::::::::::::::::::,:::,:::::,                         
             :,:::::::,,::::::::::::,,::::::,,,,::::,,,,                        
             ,::::::::,,:::::::::::,,::::::~.,,:,,,::::,                        
             ::::::::::,,:::::::::::~.,:,:,,....,:::::::,                       
            ,:::::::::::,::::::::::,:,..:~,..:::::::::::,                       
           :,::::,::::::,,:,.,,:::::,,:~~...::~~,,,.,,:::.                      
          :,:::::,::::::,,::::::::::,,,:=+++?~==:::::::::,,                     
          ::::::,,:::::::,,:::::::,.:~,~=+=~~~+=::::::::::,                     
         :,:::::,,::::,::,,::::::,,,~+++:,,~~==,:::::::::::,                    
         ,,:::::,,:::,,:::,,:::,,:::,=+++~::~+,:::::::::::::,                   
         ,:::::,,::::,,:::,,::,,:::::,~==+++=,::::::::::::::,                   
        ,::::::,,::::,,::::,,::::::::::,,,..,:::::::::::::::::                  
        ,:::::,,,,::,,::::::,,:::::::::::::::::::::::::::::::,                  
       ,,::::,,::::,,,::::::,,::::::::::::::::::::::::::::::::,                 
      :,::,.,,::::::,,,,:::::,:::::::::::::::::::::::::::::::::,    ,,...:      
      ,,::,...,::::,,,,,,::::,,:::::::::::::::::::::::::::::::::, ,,::,.:.:     
     :,::::,,:,,,,,,,,,:::::::,::::::::::::::::::::::::::::::::::,,:,,::..      
     ,:::::,,,,,,,,,::::::::::,,:::::::::::::::::::::::::::::::::::::::::       
   ::,::::::::::,,,,:::::::::::,::::::::::::::::::::::::::::::::,::,:::.::      
   :,,::::::::::::::::::::::::::....,:::::::::::::::::::::::::::,::,::.,        
   :,,:::::::::::::::::::::::,..,::,,::::::::::::::::::::::::,:::,,,,,,         
   :,,::::::::::::::::::::::,,::,,,.,,::::::::::::,,::::::::::::    ::          
   :::,,:::,,::::::::::::,,,,:,,,:::,::::::::::                                 
              :,,,:::,:,,:::,:,,::::,::::::                                     
                  :,,:::::::,:,,::::,,:::                                       
                            ,,,,:::,                                            
                            ::,,,,::                                            
                                                                                 """

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

    is_private = ipaddress.ip_address(ip).is_private
    if is_private:
        logger.info(f"{ip} is internal/private - mark as safe")
        address_safe = True
    else:
        address_safe = is_safe_address(ip, settings.VPN_KEY)
    city_region = f'{info.get("city", "Unknown")}, {info.get("region", "Unknown")}'

    logger.info(f"{ip} is visiting from {city_region} - safe? {address_safe}")
    try:
        visitor_obj = Visitor.objects.get(visitor_ip=ip)
        visitor_obj.time_visited = timezone.now()
        visitor_obj.times_visited += 1
    except Visitor.DoesNotExist:
        visitor_obj = Visitor(
            visitor_ip=ip,
            time_visited=timezone.now(),
            visitor_city_region=city_region,
            is_safe=address_safe,
            is_private=is_private,
            times_visited=1,
        )
    visitor_obj.save()
    return render(
        request,
        "zweedendev/index.html",
        {"visitor_ip": visitor_obj.visitor_ip, "server_time": timezone.now()},
    )

@api_view(["GET"])
def list_info(request):
    ip = get_client_ip(request)
    current_visitor_info = Visitor.objects.filter(visitor_ip=ip)[0]
    serializer = InfoSerializer(current_visitor_info)
    graphic = i_know_he_ate_a_cheese()
    headers = dict()
    for line_idx in range(len(graphic.splitlines())):
        headers[f"x-zweeden{line_idx}"] = graphic.splitlines()[line_idx]
    return Response(serializer.data, headers=headers)
