# Generated by Django 3.0.5 on 2020-04-04 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("zweedendev", "0003_visitor_visitor_city_region"),
    ]

    operations = [
        migrations.AlterField(
            model_name="visitor",
            name="visitor_ip",
            field=models.CharField(max_length=39),
        ),
    ]
