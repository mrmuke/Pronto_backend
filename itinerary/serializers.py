from .models import Location,Day,Schedule,Review
from rest_framework import serializers

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"

class DaySerializer(serializers.ModelSerializer):
    location_set = LocationSerializer(many=True)
    class Meta:
        model = Day
        fields = "__all__"

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"

class ScheduleSerializer(serializers.ModelSerializer):
    day_set = DaySerializer(many=True)
    review_set=ReviewSerializer(many=True)
    class Meta:
        model = Schedule
        fields = "__all__"
