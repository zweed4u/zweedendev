# Generated by Django 3.0.5 on 2020-04-08 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("zweedendev", "0007_auto_20200407_2342"),
    ]

    operations = [
        migrations.AddField(
            model_name="visitor",
            name="is_private",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="visitor",
            name="times_visited",
            field=models.IntegerField(default=1),
        ),
    ]
