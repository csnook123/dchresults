from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from .models import athlete,coaching,ranks,performances,pbs
from django.http import HttpResponse
from timeit import default_timer
import sqlite3

# Create your views here.
initialslist = ['a','b','c','d','e','f','g','h','i','j','k','l','m'
                ,'n','o','p','q','r','s','t','u','v','w','x','y','z']

def loadalldata(request):
    loadathletes('None')
    '''
    coachingload(request)
    personalbests('/personalbests/')
    performanceload('/performanceload/')
    rankingsload('/rankingsload/')
    '''
    return HttpResponse('/All Data loaded/')

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
            urlathlete = f'https://www.thepowerof10.info/athletes/profile.aspx?athleteid='
            urlathlete += f'{i.athlete_id}'
            htmlathlete = requests.get(urlathlete)
            soupathlete = BeautifulSoup(htmlathlete.text, 'html.parser')                
            coach_dets = soupathlete.find('div', {'id': 'cphBody_pnlAthletesCoached'})
            if  coach_dets is not None:
                s = coach_dets.find('table', {'class': 'alternatingrowspanel'}).find_all('tr')
                for n in s:
                    dets = n.find_all('td')
                    if dets[0].text != 'Name':
                        coach = coaching(
                            athlete_id = i,
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
            urlathlete = f'https://www.thepowerof10.info/athletes/profile.aspx?athleteid='
            urlathlete += f'{i.athlete_id}'
            htmlathlete = requests.get(urlathlete)
            soupathlete = BeautifulSoup(htmlathlete.text, 'html.parser')                
            athlete_pb = soupathlete.find('div', {'id': 'cphBody_divBestPerformances'}).find_all('tr')
            for n in athlete_pb:
                if n.find('b').text != 'Event':
                    pb = pbs(
                        athlete_id = i,
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
        try:            
            urlathlete = f'https://www.thepowerof10.info/athletes/profile.aspx?athleteid='
            urlathlete += f'{i.athlete_id}'
            htmlathlete = requests.get(urlathlete)
            soupathlete = BeautifulSoup(htmlathlete.text, 'html.parser')                
            athlete_perf = soupathlete.find('div', {'id': 'cphBody_pnlPerformances'}).find_all('table')[1].find_all('tr')
            for n in athlete_perf:
                if len(n.find_all('td')) > 1 and 'EventPerfPosVenueMeetingDate' != n.text:
                    dets = n.find_all('td')
                    perf = performances(
                        athlete_id = i,
                        event = dets[0].text,
                        value = dets[1].text,
                        position = dets[5].text,
                        raceid = dets[6].text,
                        venue = dets[9].text,
                        meeting = dets[10].text,
                        date = dets[11].text
                    )
                    perf.save()
        except:
            ''
    end = default_timer()
    return HttpResponse('Performances Saved time taken' + repr(end-start))

def rankingsload(request):
    start = default_timer()
    a = ranks.objects.all()
    a.delete()
    for i in athlete.objects.all():
        try: 
            urlathlete = f'https://www.thepowerof10.info/athletes/profile.aspx?athleteid='
            urlathlete += f'{i.athlete_id}'
            htmlathlete = requests.get(urlathlete)
            soupathlete = BeautifulSoup(htmlathlete.text, 'html.parser')                
            athlete_rank = soupathlete.find('div', {'id': 'cphBody_pnlMain'}).find('td', {'width': 220, 'valign': 'top'}).find_all('table')
            if len(athlete_rank) > 2:
                for n in athlete_rank[2].find_all('tr'):
                    dets = n.find_all('td')
                    if dets[0].text != 'Event':
                        rankings = ranks(
                            athlete_id = i,
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

    return HttpResponse('Athletes Loaded ' + str(a) +'<br>Coaching Records Loaded ' 
                        + str(b) + '<br>Rankings Loaded ' + str(c) + '<br>Performances Loaded '
                        + str(d) + '<br>PBs Loaded ' + str(e))
