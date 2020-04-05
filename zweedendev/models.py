import datetime
from django.db import models
from django.utils import timezone

# Create your models here.
class Visitor(models.Model):
    visitor_ip = models.CharField(max_length=39)  # 15 for ipv4, 39 for ipv6
    time_visited = models.DateTimeField("date visited")
    visitor_city_region = models.CharField(max_length=255, default="Unknown, Unknown")

    def visited_recently(self):
        return self.time_visited >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        # better representation than "Visitor object (n)" in admin
        return self.visitor_ip
