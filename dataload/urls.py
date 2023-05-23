from django.urls import path
from . import views


urlpatterns = [
    path("loadathletes",views.loadathletes),
    path("loadathletedetails",views.loadathletedetails)
]