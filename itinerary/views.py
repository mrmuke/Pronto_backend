from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
import itertools
import operator
import requests
import numpy as np
import json
from .routeOptimization import createSchedule
from .models import Schedule
from .serializers import ScheduleSerializer
from .flight import get_best_flight
import datetime
class GetSchedule(generics.RetrieveAPIView):

    def get(self, *args, **kwargs):
        days=int(self.request.GET.get("days"))
        city=self.request.GET.get("city").replace("-"," ")
        print(self.request.GET.get("from"))
        schedule = createSchedule(num_days=days,city=city,origin=self.request.GET.get("from"))
        
        return Response(schedule)

class ViewSchedule(generics.RetrieveAPIView):
    serializer_class = ScheduleSerializer

    def get(self, *args, **kwargs):
        id=self.kwargs["id"]
        schedule=Schedule.objects.get(id=id)
        codes={
            "Hong Kong":"HKG"
        }
        today=datetime.datetime.today()
        flight = get_best_flight(schedule.origin,codes[schedule.city],(today+datetime.timedelta(days=1)).strftime('%Y-%m-%d'),(today+datetime.timedelta(days=schedule.length+1)).strftime('%Y-%m-%d'))
        return Response({'plan': self.get_serializer(schedule, context={'request': self.request}).data,'flight':flight})

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





