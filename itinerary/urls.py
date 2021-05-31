from django.urls import path
from .views import GetJob, GetSchedule,ViewSchedule, SubmitComment,GetComment,SearchCities

urlpatterns = [
    path("getSchedule", GetSchedule.as_view()),
    path("<int:id>", ViewSchedule.as_view()),
    path("job", GetJob.as_view()),

    path("submitComment", SubmitComment.as_view()),
    path("getComments", GetComment.as_view()),
    path("getPlans", SearchCities.as_view())
]