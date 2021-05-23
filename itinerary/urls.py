from django.urls import path
from .views import GetSchedule,ViewSchedule


urlpatterns = [
    path("getSchedule", GetSchedule.as_view()),
    path("<int:id>", ViewSchedule.as_view())



]