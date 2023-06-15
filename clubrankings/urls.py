from django.urls import path
from . import views


urlpatterns = [
    path("form/<str:id>",views.profile),
    path("league_charts/<str:num>",views.league_charts),
    path("form/",views.form_view),
   ]