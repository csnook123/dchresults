from django.urls import path
from . import views


urlpatterns = [
    path("form/<str:id>",views.profile),
#    path("ranking/<str:event>",views.rankings),
#    path("ranking_charts/<str:event>",views.ranking_charts),
#    path("league_results/<str:reference>",views.league_results),
#    path("league_charts/<str:chart>",views.league_charts),
#    path("bests_by_year/<str:event>",views.bests_by_year),
#    path("suggestions",views.suggestions),
    path("form/",views.form_view),
   ]