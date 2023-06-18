from django.urls import path
from . import views


urlpatterns = [
    path("form/<str:id>",views.profile),
    path("charts/<str:num>",views.charts),
    path("form/",views.form_view),
    path("test/",views.test),
    path("test1/",views.test1),

   ]