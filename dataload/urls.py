from django.urls import path
from . import views


urlpatterns = [
    path("loadathletes",views.loadathletes),
    path("checknumbers",views.checknumbers),
   ]