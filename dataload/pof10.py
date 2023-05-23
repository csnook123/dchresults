from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from .models import athlete
from django.http import HttpResponse
from timeit import default_timer



def listathletes(request):
    a = athlete.objects.all()
    a.delete
    initialslist = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n",
                    "o","p","q","r","s","t","u","v","w","x","y","z"]

    start = default_timer()
    athleteclub = "Durham City Harriers"
    noathletes = int(0)
    for x in initialslist:
        for y in initialslist:            
            i = repr(x)
            j = repr(y)
            '''
            Returns a list of athletes with the inputted firstname or club.

            Parameters:
                    - 'club' (str): Optional club agrument

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
            noathletes = noathletes+1
   
            for r in results[1:-1]:
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
    end = default_timer()




    return HttpResponse(repr(noathletes) + ' ' + repr(end-start))




'''
                Add extra code here to retrieve further details about the athlete
                athl_id = str(row[7]).split('"')[3].split('=')[1]
                urlath = f'https://www.thepowerof10.info/athletes/profile.aspx?athleteid={athl_id}'
                htmlath = requests.get(url)
                soupath = BeautifulSoup(html.text, 'html.parser')
                athlete_dets = soupath.find('div', {'id': 'cphBody_pnlAthleteDetails'}).find_all('table')[1].text.replace('\n', '').split(':')
                athlete_abo = soupath.find('div', {'id': 'cphBody_pnlAbout'}).find_all('table')[1]
                coach_dets = soupath.find('div', {'id': 'cphBody_pnlAthletesCoached'})

                if coach_dets is not None:
                    s = coach_dets.find('table', {'class': 'alternatingrowspanel'}).find_all('tr')
                    for i in s:
                        dets = i.find_all('td')
                        if dets[0].text != 'Name':
                            coachexp_recorded = coachexp_recorded+1

                            coach = coaching(
                                athlete_id = athl_id,
                                name = dets[0].text,
                                club = dets[1].text,
                                age_group = dets[2].text,
                                sex = dets[3].text,
                                best_event = dets[4].text,
                                rank = dets[5].text,
                                age_group_rank = dets[6].text,
                                year = dets[7].text,
                                performance = dets[8].text
                                    )
                            coach.save()
                '''
