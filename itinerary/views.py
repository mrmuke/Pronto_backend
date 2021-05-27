from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
import itertools
import operator
import requests
import numpy as np
import json
from .routeOptimization import createSchedule
from .models import Schedule, Location
from .serializers import LocationSerializer, ScheduleSerializer
from .flight import get_best_flight
import datetime
class GetSchedule(generics.RetrieveAPIView):

    def get(self, *args, **kwargs):
        days=int(self.request.GET.get("days"))
        city=self.request.GET.get("city").replace("-"," ")
        print(self.request.GET.get("from"))
        schedule = createSchedule(num_days=days,city=city,origin=self.request.GET.get("from"))
        
        return Response(schedule)

class ViewSchedule(generics.RetrieveUpdateAPIView):
    serializer_class = ScheduleSerializer

    def get(self, *args, **kwargs):
        id=self.kwargs["id"]
        schedule=Schedule.objects.get(id=id)
        codes={
            "Hong Kong":"HKG"
        }
        today=datetime.datetime.today()
        flight={'OutDay': '5/27', 'OutWeekday': 'Thu', 'OutDuration': '54h03m', 'OutCities': 'MDW‐HKG', 'ReturnDay': '6/1', 'ReturnWeekday': 'Tue', 'ReturnDuration': '57h23m', 'ReturnCities': 'HKG‐MDW', 'OutStops': '3 stops', 'OutStopCities': 'TYS, BOS, ...', 'ReturnStops': '3 stops', 'ReturnStopCities': 'IST, IAH-HOU, ...', 'OutTime': '8:57 pm – 4:00 pm +3', 'OutAirline': 'Allegiant Air, Qatar Airways', 'ReturnTime': '8:57 pm – 4:00 pm +3', 'ReturnAirline': 'Turkish Airlines, Allegiant Air', 'Price': 1440}
        #flight = get_best_flight(schedule.origin,codes[schedule.city],(today+datetime.timedelta(days=1)).strftime('%Y-%m-%d'),(today+datetime.timedelta(days=schedule.length+1)).strftime('%Y-%m-%d'))
        return Response({'plan': self.get_serializer(schedule, context={'request': self.request}).data,'flight':flight})
    def put(self, request,*args, **kwargs):
        Location.objects.filter(id=self.kwargs["id"]).delete()
        serializer = LocationSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
   
            serializer.save()
        return Response("Success")
class ChangeAirport(generics.RetrieveAPIView):
    serializer_class = ScheduleSerializer

    def get(self, *args, **kwargs):
        id=self.kwargs["id"]
        schedule=Schedule.objects.get(id=id)
        codes={
            "Hong Kong":"HKG"
        }
        today=datetime.datetime.today()
        flight = get_best_flight(schedule.origin,codes[schedule.city],(today+datetime.timedelta(days=1)).strftime('%Y-%m-%d'),(today+datetime.timedelta(days=days+1)).strftime('%Y-%m-%d'))
        return Response({'plan': self.get_serializer(schedule, context={'request': self.request}).data,'flight':flight})





