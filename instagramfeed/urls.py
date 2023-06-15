from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
   path('', TemplateView.as_view(template_name='test.html', extra_context={
        "instagram_profile_name": "cian_run" }))

]
