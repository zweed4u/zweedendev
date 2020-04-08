# Generated by Django 3.0.5 on 2020-04-08 18:30
from zweedendev.models import Visitor
from django.db import migrations
from django.db import migrations


def private_is_safe(apps, schema_editor):
    visitors = Visitor.objects.filter(is_private=True)
    for visitor in visitors:
        visitor.is_safe = True
        visitor.save()


class Migration(migrations.Migration):

    dependencies = [
        ("zweedendev", "0009_auto_20200408_1319"),
    ]

    operations = [
        migrations.RunPython(private_is_safe),
    ]