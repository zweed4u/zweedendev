from django.contrib import admin
from .models import Visitor

# Register your models here.
class VisitorAdmin(admin.ModelAdmin):
    list_display = ("visitor_ip", "is_safe", "time_visited", "visitor_city_region")

    def visitor_ip(self, obj):
        return obj.visitor_ip

    def is_safe(self, obj):
        return obj.is_safe

    def time_visited(self, obj):
        return obj.time_visited

    def visitor_city_region(self, obj):
        return obj.visitor_city_region


admin.site.register(Visitor, VisitorAdmin)
