# -*- coding: utf-8 -*-
from __future__ import unicode_literals
 
from django.contrib import admin
from .models import Event
import datetime
import calendar
from django.urls import reverse
from calendar import HTMLCalendar
from django.utils.safestring import mark_safe
 
# Register your models here.
 
class EventAdmin(admin.ModelAdmin):
    list_display = ['day', 'start_time', 'end_time', 'notes']
  
 
admin.site.register(Event, EventAdmin)