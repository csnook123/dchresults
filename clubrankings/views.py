from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from  .functions import *
from .functionframesconstruction import *
from .functionbuildforms import *
# Create your views here.

# Image of Club logo and text at the top
# Divisions in the page to hold views from python
# Tables to have black and orange alternating stripes with white text

def pythonsidebar():
    frame = performancecounts()
    event_list = frame['event'].unique().tolist()
    test = dropdown(event_list)
    frame['year'] = frame['date'].apply(pd.to_datetime).dt.year
    frame = frame[frame['year'] > 2011]
    perf_frame = frame.groupby('year').sum('Performances')
    test += perf_frame.to_html()
    return test

def index(request):
    test = pythonsidebar()
    return render(request, "clubrankings/index.html", {
                  "pythonsidebar1" : test
    })
