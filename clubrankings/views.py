from django.shortcuts import render
from django.http  import HttpResponse
from .forms import *
from pandas import DataFrame
import dataload.views as dl
from bokeh.plotting import figure
from bokeh.embed import components
import datetime
import numpy as np

def make_clickable(id,val):
    return f'<a href={id}>{val}</a>'

def rankingframe():
    db = sqlite3.connect('db.sqlite3')
    rankingquery = db.cursor()
    sql = 'select event, position, 1001 - position as Harrier_League_Points, a.name as name, performance, sex,meeting, venue, date, Age_Group_Performance'
    sql += ' , club_at_performance,year,event_group, a.athlete_id, event_type,XCSeason from dataload_performances p INNER JOIN dataload_athlete a on '
    sql += 'a.athlete_id = p.athlete_id ' 
    sql += 'where club_at_performance = "Durham"'
    rankingquery.execute(sql) 
    r = pd.DataFrame(rankingquery.fetchall(), columns = [x[0] for x in rankingquery.description])
    
    return r

def league_frame():
    db = sqlite3.connect('db.sqlite3')
    league_query = db.cursor()
    #sql = 'Select * '
    #sql = 'Select count(*) '
    sql = 'Select event, race,year, event_group, pos, perf,r.athlete_id, r.name as name, age_group, r.club AS club, gender,date,meeting,venue, points '
    sql +=' from dataload_results r ' 
    sql +='INNER JOIN dataload_meets m '
    sql +=' on r.meeting_id = m.meeting_id '
#    sql +=' INNER JOIN dataload_athlete a '
#    sql +=' on a.athlete_id = r.athlete_id'    
    t = league_query.execute(sql)
    t = pd.DataFrame(t.fetchall(), columns = [x[0] for x in t.description])
    return t

def league_table():
    db = sqlite3.connect('db.sqlite3')
    league_query = db.cursor()
    #sql = 'Select * '
    #sql = 'Select count(*) '
    sql = 'Select event, race,year, event_group, pos, perf, r.name as name, age_group, r.club AS club, gender,date,meeting,venue, points '
    sql +=' from dataload_results r ' 
    sql +='INNER JOIN dataload_meets m '
    sql +=' on r.meeting_id = m.meeting_id '
    t = league_query.execute(sql)
    t = pd.DataFrame(t.fetchall(), columns = [x[0] for x in t.description])
    return t

def filter_ranking_frame(t,Year,Gender,Age_Group,Event_Group,Event,XCSeason):
        if Year != "All":
            t = t[t['year'] == Year]
        if Gender != "All":
            t = t[t['sex'] == Gender]
        if Age_Group != "All":
            t = t[t['Age_Group_Performance'] == Age_Group]
        if Event_Group != "All":
            t = t[t['event_group'] == Event_Group]
        if Event != "All":
            t = t[t['event'] == Event]
        if XCSeason != "All":
            t = t[t['XCSeason'] == XCSeason]
        return t

def filter_league_frame(t,Year,Gender,Age_Group,Event_Group,Event,League,League_Date,Clubs):
    if Year != "All":
        t = t[t['year'] == Year]
    if Gender != "All":
        t = t[t['gender'] == Gender]
    if Age_Group != "All":
        t = t[t['age_group'] == Age_Group]
    if Event_Group != "All":
        t = t[t['event_group'] == Event_Group]
    if Event != "All":
        t = t[t['event'] == Event]
    if League != "All":
        t = t[t['meeting'] == League]
    if League_Date != "All":
        t = t[t['date'] == League_Date]
    if Clubs == "no":
        t = t[t['club'] == 'Durham']
    return t


# Create your views here.
def form_view(request,*args):

    #Code to generate a form to input values and Get Options to a URL to be used as variables
    context ={}
    Age_Group = request.GET.get('Age_Group')
    Event_Group = request.GET.get('Event_Group')
    Year = request.GET.get('Year')
    Event = request.GET.get('Event')
    Gender = request.GET.get('Gender')
    League = request.GET.get('League')
    League_Date = request.GET.get('League_Date')
    XCSeason = request.GET.get('XCSeason')
    Clubs = request.GET.get('ShowAllClubs')
    Results_View = request.GET.get('Results_View')
    
    form = Results_Filter(initial={
        'Age_Group' : Age_Group,
        'Event_Group' : Event_Group,
        'Year' : Year,
        'Event': Event,
        'Gender': Gender,
        'League': League,
        'League_Date': League_Date,
        'ShowAllClubs': Clubs,
        'XCSeason': XCSeason,
        'Results_View': Results_View
    })

    context['form']= form

    if Results_View == 'Top 100 Performances':
        context['guide'] = 'The aim of this view is to show the top 100 performances in '
        context['guide'] += ' a specific event by athletes who were DCH members at the time of '
        context['guide'] += ' the performance. It will only work effectively if filtered to a  '
        context['guide'] += ' particular event and unless filtered will show a range of genders '
        context['guide'] += ' and age groups '
        t = pd.DataFrame(rankingframe(), 
                     columns = ['name','sex','venue','event','performance',
                                'date','year','event_group','Age_Group_Performance',
                                'club_at_performance'])

        t = filter_ranking_frame(t, Year,Gender,Age_Group,Event_Group,Event)
        if dl.geteventgroup(Event) in ('Throws','Jumps','Combined Events'):
            try:
                t['performance'] = t['performance'].astype(float)
            except:''                
            t = t.sort_values(['performance'], ascending=[False]).head(100)
        else:
            t = t.sort_values('performance').head(100)
        context['output'] = t.to_html()

    if Results_View == 'Best Performances':
        context['guide'] = 'The aim of this view is to show the best performance in events by '
        context['guide'] = 'athletes who were members of DCH at the time of the performance '
        context['guide'] = 'it can be filtered by year, gender, age group, event or event group '

        t = pd.DataFrame(rankingframe(), 
                     columns = ['name','sex','venue','event','performance',
                                'date','year','event_group','Age_Group_Performance',
                                'club_at_performance'])

        t = filter_ranking_frame(t,Year,Gender,Age_Group,Event_Group,Event)
        
        #Events where high is good
        options = ('Throws','Jumps','Combined Events')
        s = t[t['event_group'].isin(options)]
        s = s.sort_values("performance").groupby("event", as_index=False).first()
        
        #Events where low is good
        options = ('Barriers','Cross Country','Endurance','Running - Various', 'Running - Standard', 'Sprint')
        u = t[t['event_group'].isin(options)]
        u = u.sort_values("performance").groupby("event", as_index=False).last()
        r =  pd.concat((s,u))
        context['output'] = r.to_html()

    if Results_View == 'Top 30 Athletes':
        context['guide'] = 'The aim of this view is to show the best athletes in events '
        context['guide'] = 'according to their single best performance in a category '
        context['guide'] = 'it can be filtered by year, gender, age group, event or event group '

        t = pd.DataFrame(rankingframe(), 
                     columns = ['name','sex','venue','event','performance',
                                'date','year','event_group','Age_Group_Performance',
                                'club_at_performance'])

        t = filter_ranking_frame(t,Year,Gender,Age_Group,Event_Group,Event)
        
        #Events where high is good
        options = ('Throws','Jumps','Combined Events')
        s = t[t['event_group'].isin(options)]
        try:
            s['performance'] = s['performance'].astype(float)
        except:''                
        s = s.groupby(['event','name'], as_index=False).agg(
                Athlete_Best_Performance = ('performance','max'))
        s = s.sort_values('Athlete_Best_Performance', ascending=[False]).head(30)
        s['Rank'] = s.sort_values(by=['Athlete_Best_Performance'], ascending=False).reset_index().index + 1
        #Events where low is good
        options = ('Barriers','Cross Country','Endurance','Running - Various', 'Running - Standard', 'Sprint')
        u = t[t['event_group'].isin(options)]
        u = u.groupby(['event','name'], as_index=False).agg(
                Athlete_Best_Performance = ('performance','min'))
        u = u.sort_values('Athlete_Best_Performance').head(30)
        u['Rank'] = u.sort_values(by=['Athlete_Best_Performance']).reset_index().index + 1
        
        r =  pd.concat((s,u))
        context['output'] = r.to_html()


    if Results_View == 'Total League Points':
        context['guide'] = "The aim of this view is to show the total points accumulated for the team"
        context['guide'] += " by each DCH athlete alongside the number of events and average points per"
        context['guide'] += " event, with the option to filter by year, date of match/event group etc. "
        
        t = league_frame()
        t = filter_league_frame(t,Year,Gender,Age_Group,Event_Group,Event,League,League_Date,Clubs)
        t['Barriers'] = np.where(t['event_group']=='Barriers', t['points'], 0)
        t['Endurance'] = np.where(t['event_group']=='Endurance', t['points'], 0)
        t['Jumps'] = np.where(t['event_group']=='Jumps', t['points'], 0)
        t['Sprints'] = np.where(t['event_group']=='Sprints', t['points'], 0)
        t['Throws'] = np.where(t['event_group']=='Throws', t['points'], 0)
        t = t.groupby(['athlete_id','name','club'], as_index=False).agg(
                TotalPoints = ('points','sum'),
                TotalEvents = ('points','count'),
                AveragePoints = ('points','mean'),
                Barriers = ('Barriers','sum'),
                Endurance = ('Endurance','sum'),
                Jumps = ('Jumps','sum'),
                Sprints = ('Sprints','sum'),
                Throws = ('Throws','sum')
                
                )        
        t = t.sort_values(by='TotalPoints', ascending=False)
        t['Rank'] = t.sort_values(by=['TotalPoints']).reset_index().index + 1

        for i in range(0,len(t.index)):
            t['name'][i] = make_clickable(t['athlete_id'][i],t['name'][i])
        context['output'] = t.to_html(render_links=True,escape=False,index=False)
    
    if Results_View == 'League Tables':
        context['guide'] = "The aim of this view is to compare out performance against"
        context['guide'] += " other teams in our division."
        context['guide'] += " it doesn't include officials"
        context['guide'] += " points and currently I am struggling to get the correct teams "
        context['guide'] += " lifted from Power of 10"

        t = league_table()
        t = filter_league_frame(t,Year,Gender,Age_Group,Event_Group,Event,League,League_Date,Clubs)
        t['Barriers'] = np.where(t['event_group']=='Barriers', t['points'], 0)
        t['Endurance'] = np.where(t['event_group']=='Endurance', t['points'], 0)
        t['Jumps'] = np.where(t['event_group']=='Jumps', t['points'], 0)
        t['Sprints'] = np.where(t['event_group']=='Sprints', t['points'], 0)
        t['Throws'] = np.where(t['event_group']=='Throws', t['points'], 0)
        t = t.groupby(['club'], as_index=False).agg(
                TotalPoints = ('points','sum'),
                TotalEvents = ('points','count'),
                AveragePoints = ('points','mean'),
                Barriers = ('Barriers','sum'),
                Endurance = ('Endurance','sum'),
                Jumps = ('Jumps','sum'),
                Sprints = ('Sprints','sum'),
                Throws = ('Throws','sum')
                
                )        
        t = t.sort_values(by='TotalPoints', ascending=False)
        t['Rank'] = t.sort_values(by=['TotalPoints']).reset_index().index + 1
        context['output'] = t.to_html()

    if Results_View == 'Total Harrier League Points':
        context['guide'] = "The aim of this view is to show the total points accumulated "
        context['guide'] += " by each DCH athlete in the Start North East Harrier League"
        context['guide'] += " currently filters by Calendar year, but I need a way to filter "
        context['guide'] += " by season "
           
        r = rankingframe()
        r = filter_ranking_frame(r,Year,Gender,Age_Group,Event_Group,Event,XCSeason)
        r = r[r['meeting'] == 	'Start Fitness North Eastern Harrier League']
        r = r.groupby(['athlete_id','name'], as_index=False).agg(
                TotalPoints = ('Harrier_League_Points','sum'),
                TotalEvents = ('Harrier_League_Points','count'),
                AveragePoints = ('Harrier_League_Points','mean'))        
        r = r.sort_values(by='TotalPoints', ascending=False)
        for i in range(0,len(r.index)):
            r['name'][i] = make_clickable(r['athlete_id'][i],r['name'][i])        
        context['output'] = r.to_html(render_links=True,escape=False,index=False)


    #if athlete_id !='':
    #    t = league_frame()
    #    t = t[t['athlete_id'] == athlete_id]
    return render(request, "clubrankings/form.html", context)

def profile(request,id):
    context = {}
    t = league_frame()
    t = t[t['athlete_id']==id]
    context['guide1'] = 'An athlete profile showing performances in leagues for DCH'
    context['guide1'] += 'Begins with an initial matrix showing athletes points by year and event group'
    s = t.groupby(['year','event_group'], as_index=False).agg(
    TotalPoints = ('points','sum'))
    s = s.pivot(index = 'year', columns = 'event_group', values = 'TotalPoints')
    context['output1'] = s.to_html()
    context['guide2'] = 'Followed up by a listing of all their performances'
    context['output2'] = t.to_html()
    context['guide3'] = ''
    context['output3'] = ''
    return render(request, "clubrankings/athlete_profile.html", context)


def charts(request,num):


        #Code to generate a form to input values and Get Options to a URL to be used as variables
    context ={}
    Age_Group = request.GET.get('Age_Group')
    Event_Group = request.GET.get('Event_Group')
    Year = request.GET.get('Year')
    Event = request.GET.get('Event')
    Gender = request.GET.get('Gender')
    League = request.GET.get('League')
    League_Date = request.GET.get('League_Date')
    XCSeason = request.GET.get('XCSeason')
    Results_View = request.GET.get('Results_View')
    #athlete_id = request.Get.get('id')

    form = Charts_Filter(initial={
        'Age_Group' : Age_Group,
        'Event_Group' : Event_Group,
        'Year' : Year,
        'Event': Event,
        'Gender': Gender,
        'League': League,
        'League_Date': League_Date,
        'XCSeason':XCSeason,
        'Results_View': Results_View
    })


    if num == '1':
        t = rankingframe()
        t = filter_ranking_frame(t,Year,Gender,Age_Group,Event_Group,Event,XCSeason)


        r = t.groupby(['event'], as_index=False).agg(
        Performances = ('performance','count'))
        r = r.sort_values(['Performances'], ascending=False).head(20)

        Events = r['event'].to_list()
        Performances = r['Performances'].to_list()
        p = figure(x_range=Events, height=350, title="Top 20 Events by Number of Performances",
           toolbar_location=None, tools="")
        p.vbar(x=Events, top=Performances, width=0.9)
        p.xgrid.grid_line_color = None
        p.y_range.start = 0
        script, div = components(p)
    
    if num == '2':
        t = rankingframe()
        t = filter_ranking_frame(t,Year,Gender,Age_Group,Event_Group,Event,XCSeason)

        if Event_Group in ('Throws','Jumps','Combined Events'):
            r = t.groupby(['year'], as_index=False).agg(
            BestPerformance = ('performance','max'))
        else:
            r = t.groupby(['year'], as_index=False).agg(
            BestPerformance = ('performance','min'))
            for i in [0,len(r)]:
                    for fmt in ('%H:%M', '%H:%M:%S', '%H:%M.%S'):
                        try:
                            r['BestPerformance'][i] = datetime.datetime.strptime('02:12',fmt)
                        except:''
        Year = r['year'].to_list()
        BestPerformances = r['BestPerformance'].to_list()

        p = figure(x_range=Year, width=750, height=350, title="Best Performance in the club each year",
           toolbar_location=None, tools="")
        p.vbar(x=Year, top=BestPerformances, width=0.9)
        p.xgrid.grid_line_color = None
        p.y_range.start = 0
        script, div = components(p)

    if num == '3':
        t = rankingframe()
        t = filter_ranking_frame(t,Year,Gender,Age_Group,Event_Group,Event,XCSeason)


        r = t.groupby(['year'], as_index=False).agg(
        Performances = ('performance','count'))

        year = r['year'].to_list()
        Performances = r['Performances'].to_list()
        p = figure(x_range=year, height=350, title="Number of Performances each year",
           toolbar_location=None, tools="")
        p.vbar(x=year, top=Performances, width=0.9)
        p.xgrid.grid_line_color = None
        p.y_range.start = 0
        script, div = components(p)



    return render(request, 'clubrankings/bokeh.html',  {'form': form, 'script': script, 'div': div})

def test(request):
    r = rankingframe()
#    r = r[r['event'] == 'HT7.26K']
    return HttpResponse(r.to_html())


def test1(request):
    return HttpResponse()
