from django.urls import path
from . import views


urlpatterns = [
    path("",views.index),
    path("<str:event>",views.rankings,name="event-rankings"),
    #path("testingstuff",views.testingstuff),
   ]