from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
import itertools
import operator
import requests
import numpy as np
import json
from .routeOptimization import createSchedule
from .models import Schedule, Location,Review
from .serializers import LocationSerializer, ScheduleSerializer
from .flight import get_best_flight
import datetime
from rest_framework.views import APIView
codes={
            "Hong Kong":"HKG",
            "Maui": "OGG",
            "Bangkok":"DMK",
            "London":"YXU",
            "Macau":"MFM",
            "Singapore":"SIN",
            "Paris":"LBG",
            "Tahiti":"PPT",
            "Tokyo":"NRT",
            "Rome":"CIA",
            "Phuket":"HKT",
            "Barcelona":"BCN",
            "Bali":"DPS",
            "Dubai":"DXB",
            "New York City":"JFK"
        }
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
        
        today=datetime.datetime.today()
        
        #flight={'OutDay': '5/27', 'OutWeekday': 'Thu', 'OutDuration': '54h03m', 'OutCities': 'MDW‐HKG', 'ReturnDay': '6/1', 'ReturnWeekday': 'Tue', 'ReturnDuration': '57h23m', 'ReturnCities': 'HKG‐MDW', 'OutStops': '3 stops', 'OutStopCities': 'TYS, BOS, ...', 'ReturnStops': '3 stops', 'ReturnStopCities': 'IST, IAH-HOU, ...', 'OutTime': '8:57 pm – 4:00 pm +3', 'OutAirline': 'Allegiant Air, Qatar Airways', 'ReturnTime': '8:57 pm – 4:00 pm +3', 'ReturnAirline': 'Turkish Airlines, Allegiant Air', 'Price': 1440}
        flight = get_best_flight(schedule.origin,codes[schedule.city],(today+datetime.timedelta(days=1)).strftime('%Y-%m-%d'),(today+datetime.timedelta(days=schedule.length+1)).strftime('%Y-%m-%d'))
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

        today=datetime.datetime.today()
        flight = get_best_flight(schedule.origin,codes[schedule.city],(today+datetime.timedelta(days=1)).strftime('%Y-%m-%d'),(today+datetime.timedelta(days=days+1)).strftime('%Y-%m-%d'))
        return Response({'plan': self.get_serializer(schedule, context={'request': self.request}).data,'flight':flight})

class SubmitComment(APIView):
    def post(self, request, format=None):
        if(request.method == "POST"):
            data = json.loads(request.body.decode("UTF-8"))
            schedule = Schedule.objects.get(id=data["id"])
            curReview = Review(name=data["name"], comment=data["comment"], rating=data["rating"],schedule=schedule)
            curReview.save()
            return Response("success")

class GetComment(APIView):
    def post(self, request, format=None):
        review = Review.objects.filter(schedule_id=json.loads(request.body.decode("UTF-8"))["id"])
        arr = []
        for obj in review:
            arr.append({
                "comment": obj.comment,
                "name": obj.name,
                "rating": obj.rating
            })
        print(arr)
        return Response({"reviews": arr})

class SearchCities(APIView):
    def post(self, request, format=None):
        city = json.loads(request.body.decode("UTF-8"))["city"]
        if(city == "all"):
            schedules = Schedule.objects.all()[:30]
        else:
            schedules = Schedule.objects.filter(city__icontains=city)
        arr = []
        for schedule in schedules:
            review = Review.objects.filter(schedule_id=schedule.id)
            total = 0
            for obj in review:
                total+=obj.rating
            if(len(review) != 0):
                total = total/(len(review))
            display_img=""
            with open('./cityInformation.json') as f:
                display_img = json.load(f)[schedule.city]["images"][0]
                print(display_img)
            arr.append({
                "id": schedule.id,
                "city":schedule.city,
                "length":schedule.length,
                "departure":schedule.departure,
                "arrvial":schedule.arrival,
                "hotel":schedule.hotel,
                "transportation":schedule.transportation,
                "origin":schedule.origin,
                "rating":total,
                "comments": len(review),
                "image":display_img
            })
        return Response({"Schedules": arr})