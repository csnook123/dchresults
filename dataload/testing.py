from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from .models import athlete
from django.http import HttpResponse
from timeit import default_timer

# Create your views here.
initialslist = [
        "a","b","c","d","e","f","g","h","i","j","k","l","m","n",
        "o","p","q","r","s","t","u","v","w","x","y","z"  
    ],


def loadathletes(request):
    a = athlete.objects.all()
    a.delete()
 
    start = default_timer()
    athleteclub = "Durham City Harriers"
    noathletes = int(0)
    for firstinitial in range(3):
        for secondinitial in range(3):
            i = repr(initialslist[firstinitial])
            j = repr(initialslist[secondinitial])
        '''
        Returns a list of athletes with the inputted firstname or club.

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
        results = soup.find('div', {'id': 'cphBody_pnlResults'}).find_all('tr')
    
        for r in results[1:-1]:
            try:                
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
                noathletes = noathletes+1
                ath.save()
            except:
                noathletes = noathletes
    end = default_timer()

    return HttpResponse(repr(noathletes) + ' ' + repr(end-start))
