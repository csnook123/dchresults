from django.shortcuts import render
from dataload.models import athlete, performances
from django.http import HttpResponse
from django.urls import reverse
import sqlite3
import pandas as pd

db = sqlite3.connect('db.sqlite3')
rankingquery = db.cursor()

#sql = 'select * from dataload_performances'
#sql = 'select * from dataload_athlete'

sql = 'select event, firstname, surname, performance, meeting, venue, date, Age_Group_Performance'
sql += ' , club_at_performance from dataload_performances p INNER JOIN dataload_athlete a on '
sql += 'a.athlete_id = p.athlete_id'
rankingquery.execute(sql) 

r = pd.DataFrame(rankingquery.fetchall(), columns = [x[0] for x in rankingquery.description])

def make_clickable(val):
    return f'<a href="{val}">{val}</a>'

# Create your views here.
def rankings(request,event):
    s = pd.DataFrame(r,columns=['event','firstname','surname','performance','meeting','venue','date','Age_Group_Performance','club_at_performance'])
    s = s[s['event'] == event]

    rankingtable = s.to_html()
    
    return HttpResponse(rankingtable)

def index(request):

    s = r.groupby(['event'], as_index=False)[['performance']].count()
    s = s.sort_values(by='performance', ascending=False)
    for i in range(0,len(s.index)):
        s['event'][i] = make_clickable(s['event'][i])

    return HttpResponse(s.to_html(render_links=True, escape=False, index=False))

