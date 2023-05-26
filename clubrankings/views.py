from django.shortcuts import render
from dataload.models import athlete, performances
from django.http import HttpResponse
from django.urls import reverse
import sqlite3
import pandas as pd


# Create your views here.
def rankings(request,event):
    db = sqlite3.connect('db.sqlite3')
    rankingquery = db.cursor()
    rankingquery.execute('select *  from dataload_performances where dataload_performances.event = "'
                         + event + '"')
    e = pd.DataFrame(rankingquery.fetchall())
    rankingtable = e.to_html
 
    return HttpResponse(rankingtable)


def index(request):
    db = sqlite3.connect('db.sqlite3')
    eventlist = db.cursor()
    eventlist.execute('select distinct dataload_performances.event  from dataload_performances order by '
                 + 'dataload_performances.event asc')
    e = pd.DataFrame(eventlist.fetchall())

    response_data = "<li>Event</li>"
    for i in range(0,len(e.index)):
        j = e[0].values[i]
        i_path = reverse("event-rankings",args=[j])
        response_data +=f"<li><a href=\"{i_path}\">{j}</a></li>"
    return HttpResponse(response_data)