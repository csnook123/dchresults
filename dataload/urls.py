from django.urls import path
from . import views


urlpatterns = [
    path("loadalldata",views.loadalldata),
    path("loadathletes",views.loadathletes),
    path("personalbests",views.personalbests),
    path("rankingsload",views.rankingsload),
    path("performanceload",views.performanceload),
    path("coachingload",views.coachingload),
    path("checknumbers",views.checknumbers),
    path("events_load",views.events_load),
    path("events_results_load",views.event_results_load),

   ]