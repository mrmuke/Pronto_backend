from django.db import models
import math
from django.utils.timezone import now
class Schedule(models.Model):
    city = models.CharField(max_length=100)
    length=models.PositiveSmallIntegerField(default=3)
    departure=models.DateTimeField(default=now, blank=True)
    arrival=models.DateTimeField(default =now, blank=True)
    hotel=models.CharField(max_length=100, default="")
    transportation=models.CharField(max_length=200, default="")
    origin=models.CharField(max_length=100,default="SIN")

class Day(models.Model):
    schedule=models.ForeignKey(Schedule, on_delete=models.CASCADE)

class Location(models.Model):
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    lat=models.FloatField(default=0.0)
    lng=models.FloatField()
    name=models.CharField(max_length=100)
    type=models.CharField(max_length=100)
    order = models.IntegerField(default=0)

    def distance(self,location):
        lat1, lon1 = self.lat,self.lng
        lat2, lon2 = location.lat,location.lng
        radius = 6371  # km

        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
            math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
            math.sin(dlon / 2) * math.sin(dlon / 2))
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        d = radius * c

        return d
    class Meta:
        ordering = ["order"]

class Review(models.Model):
    comment= models.CharField(max_length=500)
    rating = models.SmallIntegerField()
    schedule=models.ForeignKey(Schedule,on_delete=models.CASCADE)
    
