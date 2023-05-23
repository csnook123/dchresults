from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from .models import athlete
from django.http import HttpResponse
from timeit import default_timer
import sqlite3

# Create your views here.
initialslist = ['a','b','c','d','e','f','g','h','i','j','k','l','m'
                ,'n','o','p','q','r','s','t','u','v','w','x','y','z']

def loadathletes(request):
    start = default_timer()
    a = athlete.objects.all()
    a.delete() 
    athleteclub = "Durham City Harriers"
    noathletes = int(0)
    '''
    currently have an issue whereby if a single athlete is returned
    for a set of initials they are not loaded into the database
    conversely if we go on first or last initial only we get
    too many records returned and power of 10 shuts down the connection.
    trying to handle this in the short term by capturing failed initials
    '''
    failedinitials = ''
    for x in initialslist:
        for y in initialslist:    
            i = str(x)
            j = str(y)
            '''
            Saves a list of athletes associated with DCH to the database.
            Returns:
                    - 'list_of_athletes' (arr): List of athlete data in dict
                        - 'firstname' (str): First name of athlete
                        - 'surname' (str): Surname of athlete
                        - 'track' (str): Age group for athlete on track 
                        - 'road' (str): Age group for athlete on road
                        - 'sex' (str): Gender of athlete
                        - 'club' (str): Athletics club of althete
                        - 'athlete_id' (int): Reference id of athlete (used by PowerOf10)
            '''
            url = f'https://www.thepowerof10.info/athletes/athleteslookup.aspx?'
            url += f'surname={j.replace(" ","+")}&'
            url += f'firstname={i.replace(" ","+")}&'
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
                failedinitials += i + j
    end = default_timer()
    return HttpResponse(repr(noathletes) + ' ' + repr(end-start)+ ' ' + failedinitials)

def checknumbers(request):
    db = sqlite3.connect('db.sqlite3')
    iterator = db.cursor()
    iterator.execute('select * from dataload_athlete')
    x = 0
    for i in iterator.fetchall():
        x = x+1

    return HttpResponse(x)