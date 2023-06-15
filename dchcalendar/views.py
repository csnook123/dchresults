from .models import Event
from django.http import HttpResponse
import sqlite3
import pandas as pd

def index(request):
    db = sqlite3.connect('db.sqlite3')
    events = db.cursor()
    sql = 'select *'
    sql += 'from dchcalendar_Event p'
    events.execute(sql) 
    event_list = pd.DataFrame(events.fetchall(), columns = [x[0] for x in events.description])
    ret = event_list.to_html()
    return HttpResponse(ret)