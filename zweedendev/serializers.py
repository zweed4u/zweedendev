from rest_framework import serializers
from zweedendev.models import Visitor


class InfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visitor
        fields = (
            "visitor_ip",
            "is_safe",
            "time_visited",
            "visitor_city_region",
            "is_private",
            "times_visited",
        )
