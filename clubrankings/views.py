from django.shortcuts import render
from dataload.models import athlete, performances
from django.http import HttpResponse
from django.urls import reverse
import sqlite3
import pandas as pd
import matplotlib as mpl

# Create your views here.

def index(request):
    return render(request, 'clubrankings/index.html')

def league_frame():
    db = sqlite3.connect('db.sqlite3')
    league_query = db.cursor()
    #sql = 'Select * '
    #sql = 'Select count(*) '
    sql = 'Select event, race, pos, perf, r.name as name, age_group,r.athlete_id, r.club AS club, gender,date,meeting,venue, points '
    sql +=' from dataload_results r ' 
    sql +='INNER JOIN dataload_meets m '
    sql +=' on r.meeting_id = m.meeting_id '
    sql +=' INNER JOIN dataload_athlete a '
    sql +=' on a.athlete_id = r.athlete_id'    
    t = league_query.execute(sql)
    t = pd.DataFrame(t.fetchall(), columns = [x[0] for x in t.description])
    return t


def league_frame2():
    db = sqlite3.connect('db.sqlite3')
    league_query = db.cursor()
    #sql = 'Select * '
    #sql = 'Select count(*) '
    sql = 'Select event, race, pos, perf, r.name as name, age_group,r.athlete_id, r.club AS club, gender,date,meeting,venue, points '
    sql +=' from dataload_results r ' 
    sql +='INNER JOIN dataload_meets m '
    sql +=' on r.meeting_id = m.meeting_id '
    t = league_query.execute(sql)
    t = pd.DataFrame(t.fetchall(), columns = [x[0] for x in t.description])
    return t


def event_type():
    field = [

    ]

def rankingframe():
    db = sqlite3.connect('db.sqlite3')
    rankingquery = db.cursor()
    sql = 'select event, a.name as name, performance, sex,meeting, venue, date, Age_Group_Performance'
    sql += ' , club_at_performance from dataload_performances p INNER JOIN dataload_athlete a on '
    sql += 'a.athlete_id = p.athlete_id ' 
    sql += 'where club_at_performance LIKE "%Durham%"'
    rankingquery.execute(sql) 
    r = pd.DataFrame(rankingquery.fetchall(), columns = [x[0] for x in rankingquery.description])
    
    return r

def make_clickable(val):
    return f'<a href="{val}">{val}</a>'

def rankings(request,event):
    s = pd.DataFrame(rankingframe(),columns=['event','firstname','surname','performance','meeting','venue','date','Age_Group_Performance','club_at_performance'])
    s = s[s['event'] == event]

    rankingtable = s.to_html()
    
    return HttpResponse(rankingtable)

def ranking(request):
    r = rankingframe()
    s = r.groupby(['event'], as_index=False)[['performance']].count()
    s = s.sort_values(by='performance', ascending=False)
    s['bests_by_year'] = 'bests_by_year/' + s['event']
    s['bests_by_year'] = s['bests_by_year'].apply(lambda x: f'<a href="{x}">{x}</a>')
    s['ranking'] = 'ranking/' + s['event']
    s['ranking'] = s['ranking'].apply(lambda x: f'<a href="{x}">{x}</a>')
    output = s.to_html(render_links=True, escape=False, index=False),
    pagename = "Number of performance by event and links to best by year and top 10 listings"
    return render(request, "clubrankings/rankings.html", {
        "text" : output,
        "pagename" : pagename
    })


def league_results(request,reference):
    if reference == '1': 
        t = league_frame()
        response = t.to_html()
    if reference == '2': 
        t = league_frame2()
        response = t.to_html()
    return HttpResponse(response)

def league_charts(request,chart):

    if chart == '1':
        t = pd.DataFrame(league_frame(), columns = ['name','points'])
        t = t.groupby(['name'], as_index=False).agg(
                TotalPoints = ('points','sum'),
                TotalEvents = ('points','count'),
                AveragePoints = ('points','mean'))        
        t = t.sort_values(by='TotalPoints', ascending=False)
        #t['points per event'] = t['points']/t['no of points'] 
        for i in range(0,len(t.index)):
            t['name'][i] = make_clickable(t['name'][i])
        response = t.to_html(render_links=True,escape=False,index=False)

    if chart == '2':
        t = pd.DataFrame(league_frame(), columns = ['name','date','points'])
        t = t.groupby(['name','date'], as_index=False).sum()
        t = t.pivot_table(['points'],index=['name'],columns='date')

        t = t.fillna(0)
        response = t.to_html()
        
    if chart == '3':
        t = pd.DataFrame(league_frame(), columns = ['name','date','points'])
        t = t.groupby(['name','date'], as_index=False).sum()
        t = t.pivot_table(['points'],index=['name'],columns='date')
        t = t.fillna(0)
        response = t.to_html()
    
    return HttpResponse(response)

def bests_by_year(request,event):
    t = pd.DataFrame(rankingframe(), columns = ['firstname','surname','sex','event','performance','date'])
    t['year'] = t['date'].apply(pd.to_datetime).dt.year
    t = t[t['event'] == event]
    t = t[t['sex'] == 'M']
    t = t.drop(columns = ['date','sex'])
    # need to handle the name better in rankings. 
    # t = t.groupby(['year','firstname','surname'] as_index=False).min()
    t = t.groupby(['year']).min()

    output = t.to_html(render_links=True, escape=False, index=False),
    pagename = "Best performances for each year for " + str(event)
    
    return render(request, "clubrankings/rankings.html", {
        "text" : output,
        "pagename" : pagename
    })

   
 
    # creating the bar plot
    #plt = mpl.figure()
    #plt.bar(t['year'], t['performance'], color ='maroon',
    #    width = 0.4)
    #plt.xlabel("Year")
    #plt.ylabel("Top Performance")
    #plt.title("Top Performances for DCH")
    
    #aggregate by min of performance (max for field events)
    #take top one and top ten?
    #plot over time in a bar chart


def ranking_charts(request,event, sex):
    t = pd.DataFrame(rankingframe(), columns = ['name','sex','event','performance','date'])
    t['year'] = t['date'].apply(pd.to_datetime).dt.year
    t = t[t['event'] == event]
    t = t[t['sex'] == sex]
    t = t.drop(columns = ['event','date','sex'])
    t = t.groupby(['year']).min()


    response = t.to_html()
    return HttpResponse(response)


def suggestions(request):

    return HttpResponse("Suggestion Page Not built yet")