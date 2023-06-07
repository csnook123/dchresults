from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from .models import athlete,coaching,ranks,performances,pbs,meets,results
from django.http import HttpResponse
from timeit import default_timer
from datetime import datetime
import sqlite3

# Create your views here.
initialslist = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

def league_points_calc(heat,position):
        r=0
        if position == "1": r = 9 
        if position == "2": r = 7 
        if position == "3": r = 6 
        if position == "4": r = 5 
        if position == "5": r = 4 
        if position == "6": r = 3 
        if heat == "B" and r != 0: r = r-2
        if heat == 'nsA': r =0
        return  r


def loadalldata(request):
    start = default_timer()
    loadathletes()
    performanceload()
    coachingload()
    personalbests()
    rankingsload()
    end = default_timer()
    return HttpResponse('All Data loaded  '  + repr(end-start))

def loadathletes(request):
    start = default_timer()
    a = athlete.objects.all()
    a.delete() 
    athleteclub = "Durham City Harriers"
    noathletes = int(0)
  
    failedinitials = ''
    for y in initialslist:    
            j = str(y)
            url = f'https://www.thepowerof10.info/athletes/athleteslookup.aspx?'
            url += f'surname={j.replace(" ","+")}&'
            url += f'club={athleteclub.replace(" ","+")}'
    
            html = requests.get(url)
            soup = BeautifulSoup(html.text, 'html.parser')
            try:
                results = soup.find('div', {'id': 'cphBody_pnlResults'}).find_all('tr')       
                for r in results[1:-1]:
                    noathletes = noathletes+1
                    row = BeautifulSoup(str(r), 'html.parser').find_all('td')
                    ath = athlete(
                            firstname = row[0].text, 
                            surname = row[1].text,
                            name = row[0].text + ' ' + row[1].text,
                            track = row[2].text,
                            road = row[3].text,
                            xc = row[4].text,
                            sex = row[5].text,
                            club = row[6].text,
                            athlete_id = str(row[7]).split('"')[3].split('=')[1]
                    )
                    ath.save()
            except:
                failedinitials +=' '+ j
    end = default_timer()
    return HttpResponse(repr(noathletes) + ' ' + repr(end-start)+ ' ' + failedinitials)

def coachingload(request):
    start = default_timer()
    a = coaching.objects.all()
    a.delete()
    for i in athlete.objects.all():
        try:            
            b = getattr(i,'athlete_id')
            urlathlete = f'https://www.thepowerof10.info/athletes/profile.aspx?athleteid='
            urlathlete += f'{b}'
            htmlathlete = requests.get(urlathlete)
            soupathlete = BeautifulSoup(htmlathlete.text, 'html.parser')                
            coach_dets = soupathlete.find('div', {'id': 'cphBody_pnlAthletesCoached'})
            if  coach_dets is not None:
                s = coach_dets.find('table', {'class': 'alternatingrowspanel'}).find_all('tr')
                for n in s:
                    dets = n.find_all('td')
                    if dets[0].text != 'Name':
                        coach = coaching(
                            athlete_id = b,
                            name = dets[0].text,
                            club = dets[1].text,
                            age_group = dets[2].text,
                            sex = dets[3].text,
                            best_event = dets[4].text,
                            rank = dets[5].text,
                            year = dets[7].text,
                            performance = dets[8].text
                        )
                        coach.save()
        except:
            ''    
    end = default_timer()
    return HttpResponse('CoachingLoaded time taken ' + repr(end-start))

def personalbests(request):
    start = default_timer()
    a = pbs.objects.all()
    a.delete()
    for i in athlete.objects.all():
        try:
            b = getattr(i,'athlete_id')
            urlathlete = f'https://www.thepowerof10.info/athletes/profile.aspx?athleteid='
            urlathlete += f'{b}'
            htmlathlete = requests.get(urlathlete)
            soupathlete = BeautifulSoup(htmlathlete.text, 'html.parser')                
            athlete_pb = soupathlete.find('div', {'id': 'cphBody_divBestPerformances'}).find_all('tr')
            for n in athlete_pb:
                if n.find('b').text != 'Event':
                    pb = pbs(
                        athlete_id = b,
                        event = n.find('b').text,
                        value = n.find_all('td')[1].text
                    )
                    pb.save()
        except:
            ''
    end = default_timer()           
    return  HttpResponse('Personal Bests time taken' + repr(end-start))

def performanceload(request):
    start = default_timer()
    a = performances.objects.all()
    a.delete()
    for i in athlete.objects.all():
  #      try:
            b = getattr(i,'athlete_id')
            urlathlete = f'https://www.thepowerof10.info/athletes/profile.aspx?athleteid='
            urlathlete += f'{b}'
            htmlathlete = requests.get(urlathlete)
            soupathlete = BeautifulSoup(htmlathlete.text, 'html.parser')                
            athlete_perf = soupathlete.find('div', {'id': 'cphBody_pnlPerformances'}).find_all('table')[1].find_all('tr')
            for n in athlete_perf:
                if len(n.find_all('td')) == 1:
                    dets = n.find_all('td')
                    clubs = dets[0].text
                if clubs.__contains__('Durham'):
                    clubs = 'Durham'
                else: clubs = 'Not Durham'    
                if len(n.find_all('td')) > 1 and 'EventPerfPosVenueMeetingDate' != n.text:
                    dets = n.find_all('td')
                    dateformatting = dets[11].text
                    dateformatting = datetime.strptime(dateformatting, "%d %b %y")
                    perf = performances(
                        athlete_id = b,
                        event = dets[0].text,
                        performance = dets[1].text,
                        position = dets[5].text,
                        raceid = dets[6].text,
                        venue = dets[9].text,
                        meeting = dets[10].text,
                        date = dateformatting,
                        club_at_performance = clubs,
                        Age_Group_Performance = clubs[5:8:1]
                    )
                    perf.save()
 #       except:
 #           ''
    end = default_timer()
    return HttpResponse('Performances Saved time taken' + repr(end-start))

def rankingsload(request):
    start = default_timer()
    a = ranks.objects.all()
    a.delete()
    for i in athlete.objects.all():
        try: 
            b = getattr(i,'athlete_id')
            urlathlete = f'https://www.thepowerof10.info/athletes/profile.aspx?athleteid='
            urlathlete += f'{b}'
            htmlathlete = requests.get(urlathlete)
            soupathlete = BeautifulSoup(htmlathlete.text, 'html.parser')                
            athlete_rank = soupathlete.find('div', {'id': 'cphBody_pnlMain'}).find('td', {'width': 220, 'valign': 'top'}).find_all('table')
            if len(athlete_rank) > 2:
                for n in athlete_rank[2].find_all('tr'):
                    dets = n.find_all('td')
                    if dets[0].text != 'Event':
                        rankings = ranks(
                            athlete_id = b,
                            event = dets[0].text,
                            age_group = dets[2].text,
                            year = dets[3].text,
                            rank = dets[4].text
                        )    
                        rankings.save()
        except:
            ''
    end = default_timer()
    return HttpResponse('Rankings Loaded time taken ' + repr(end-start))

def checknumbers(request):
    db = sqlite3.connect('db.sqlite3')
    iterator = db.cursor()
    iterator.execute('select * from dataload_athlete')
    a = 0
    for i in iterator.fetchall():
        a = a+1

    iterator.execute('select * from dataload_coaching')
    b = 0
    for i in iterator.fetchall():
        b = b+1

    iterator.execute('select * from dataload_ranks')
    c = 0
    for i in iterator.fetchall():
        c = c+1

    iterator.execute('select * from dataload_performances')
    d = 0
    for i in iterator.fetchall():
        d = d+1

    iterator.execute('select * from dataload_pbs')
    e = 0
    for i in iterator.fetchall():
        e = e+1

    iterator.execute('select * from dataload_meets')
    f = 0
    for i in iterator.fetchall():
        f = f+1

    iterator.execute('select * from dataload_results')
    g = 0
    for i in iterator.fetchall():
        g = g+1

    links = '<br><a href=loadathletes>Load Athletes</a>'
    links += '<br><a href=coachingload>Load Coaching Records</a>'
    links += '<br><a href=performanceload>Load Performances</a>'
    links += '<br><a href=personalbests>Load PBs</a>'
    links += '<br><a href=events_load>Load Meets</a>'
    links += '<br><a href=events_results_load>Load Results</a>'
    links += '<br><a href=rankings>Load Rankings</a>'
    

    return HttpResponse('Athletes Loaded ' + str(a) +'<br>Coaching Records Loaded ' 
                        + str(b) + '<br>Rankings Loaded ' + str(c) + '<br>Performances Loaded '
                        + str(d) + '<br>PBs Loaded ' + str(e)+ '<br>Meets Loaded ' + str(f)
                        + '<br>Results Loaded ' + str(g) + links)


def events_load(request):
    meetings =['Northern Track %26 Field League North East Premier',
               'Northern League - North East 1',
               'North East Youth Development League - Division 2',
               'North Eastern Youth Development League Division 2S']

#meeting=None, venue=None, date_from=None, year=None, date_to=None, meeting_type=None, terrain=None):

    start = default_timer()
    a = meets.objects.all()
    a.delete()
    
    for x in meetings:
        url = 'https://www.thepowerof10.info/results/resultslookup.aspx?'
        m = str(x)
        url += f'title={m.replace(" ","+")}&'
        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'html.parser')

        try:
            table = soup.find('table', {'id': 'cphBody_dgMeetings'}).find_all('tr')
        except Exception as e:
            ''
        for i in table:
            dets = i.find_all('td')
            if dets[0].text != 'Date':
                dateformatting = dets[0].text
                dateformatting = dateformatting[4:len(dets[0].text):1]
                dateformatting = datetime.strptime(dateformatting, "%d %b %Y")
                n = meets(
                        date = dateformatting,
                        meeting = dets[1].text.replace('\n','').replace('\r','').replace('     ','').replace('Info',''),
                        venue = dets[2].text,
                        type = dets[3].text,
                        meeting_id = str(dets[2]).split('"')[1].split('=')[1]
                    )
                n.save()
    end = default_timer()
    return HttpResponse('Meet Loaded ' + repr(end-start))

def event_results_load(request):
    a = results.objects.all()
    a.delete()
    start = default_timer()
    a = meets.objects.all()

    for competitions in a:
        try:
            j = competitions.meeting_id
            url = f'https://www.thepowerof10.info/results/results.aspx?meetingid={j}'
            html = requests.get(url)
            soup = BeautifulSoup(html.text, 'html.parser')
            meeting_dets = soup.find('div', {'id': 'pnlMainGeneral'}).find_all('table')[0].find('span')
            meeting_res = soup.find('table', {'id': 'cphBody_dgP'}).find_all('tr')[1:]
            count = -1
            for i in meeting_res:
                dets = i.find_all('td')
                if len(dets) == 1 and '\xa0' not in str(dets[0]):
                    vals = str(dets[0].text).split(" ")
                    count += 1            
                else:
                    if '\xa0' not in str(dets[0]) and 'Pos' not in str(dets[0].text) :
                        race = vals[2] if len(vals)>2 else 1
                        posn = dets[0].text
                        try:
                            r = results(
                                meeting_id = j,
                                event = vals[0],
                                event_age_group = vals[1],
                                race = vals[2] if len(vals)>2 else 1,
                                pos = dets[0].text,
                                perf = dets[1].text,
                                name = dets[2].text,
                                age_group = dets[4].text,
                                gender = dets[5].text,
                                club = dets[7].text,
                                athlete_id = str(dets[2]).split('"')[1].split('=')[1] if len(str(dets[2]).split('"')) > 1 else '',
                                points = league_points_calc(str(race),str(posn)),
                            )
                            r.save()
                        except:
                            r = results(
                                meeting_id = j,
                                event = vals[0],
                                event_age_group = vals[1],
                                race = vals[2] if len(vals)>2 else 1,
                                pos = dets[0].text,
                                perf = dets[1].text,
                                name = dets[3].text,
                                age_group = dets[5].text,
                                gender = dets[6].text,
                                club = dets[8].text,
                                athlete_id = str(dets[3]).split('"')[1].split('=')[1] if len(str(dets[3]).split('"')) > 1 else '',
                                points = league_points_calc(str(race),str(posn)),
                            )  
                            r.save()
        except:''
    end = default_timer()
    return HttpResponse('Meet Loaded ' + repr(end-start))
