# Generated by Django 3.0.5 on 2020-04-08 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("zweedendev", "0005_auto_20200403_2142"),
    ]

    operations = [
        migrations.AddField(
            model_name="visitor",
            name="is_safe",
            field=models.BooleanField(default=False),
        ),
    ]
