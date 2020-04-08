# Generated by Django 3.0.5 on 2020-04-08 03:42
import ipaddress
import requests
from zweedendev.models import Visitor
from django.db import migrations
from django.conf import settings


def resolve_safety(apps, schema_editor):
    key = settings.VPN_KEY
    unsafe_visitor = Visitor.objects.filter(is_safe=False)
    for visitor in unsafe_visitor:
        ip = visitor.visitor_ip
        is_private = ipaddress.ip_address(ip).is_private
        if is_private:
            continue
        try:
            response = requests.get(
                f"http://v2.api.iphub.info/ip/{ip}", headers={"X-Key": key}
            )
            block = response.json()["block"] == 0
            visitor.is_safe = block
            visitor.save()
        except Exception as e:
            print(e)
            continue


class Migration(migrations.Migration):

    dependencies = [
        ("zweedendev", "0006_visitor_is_safe"),
    ]

    operations = [
        migrations.RunPython(resolve_safety),
    ]