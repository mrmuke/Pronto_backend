from django.urls import path
from .views import DictionaryAdjectivesDestination, GetCity#,AdjectivesDestination


urlpatterns = [
	#path("adjectivesDestination", AdjectivesDestination.as_view()),
    path("dictionaryDestination", DictionaryAdjectivesDestination.as_view()),
    path("city", GetCity.as_view())
]