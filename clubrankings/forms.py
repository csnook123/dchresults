from __future__ import unicode_literals
from django import forms
from pandas import DataFrame
import sqlite3
import pandas as pd
import dataload.views as dl

def event():
    db = sqlite3.connect('db.sqlite3')
    rankingquery = db.cursor()
    sql = 'select distinct event, event as event2 '
    sql += 'from dataload_performances'
    sql += ' where club_at_performance LIKE "%Durham%"'
    rankingquery.execute(sql) 
    r = pd.DataFrame(rankingquery.fetchall(), columns = [x[0] for x in rankingquery.description])
    r = r.sort_values('event')
    r.loc[-1] = ['All','All']  # adding a row
    r.index = r.index + 1  # shifting index
    r =r.sort_index()

    event = tuple(r.itertuples(index=False, name=None))
    return event

def year():
    db = sqlite3.connect('db.sqlite3')
    rankingquery = db.cursor()
    sql = 'select distinct year, year as event2 '
    sql += 'from dataload_performances'
    sql += ' where club_at_performance LIKE "%Durham%"'
    rankingquery.execute(sql) 
    r = pd.DataFrame(rankingquery.fetchall(), columns = [x[0] for x in rankingquery.description])
    r = r.sort_values('year')
    r.loc[-1] = ['All','All']  # adding a row
    r.index = r.index + 1  # shifting index
    r =r.sort_index()
    event = tuple(r.itertuples(index=False, name=None))
    return event

def event_group():
    db = sqlite3.connect('db.sqlite3')
    rankingquery = db.cursor()
    sql = 'select distinct event_group, event_group as event2 '
    sql += 'from dataload_performances'
    sql += ' where club_at_performance LIKE "%Durham%"'
    rankingquery.execute(sql) 
    r = pd.DataFrame(rankingquery.fetchall(), columns = [x[0] for x in rankingquery.description])
    r = r.sort_values('event_group')
    r.loc[-1] = ['All','All']  # adding a row
    r.index = r.index + 1  # shifting index
    r =r.sort_index()
    event = tuple(r.itertuples(index=False, name=None))
    return event

def age_group():
    db = sqlite3.connect('db.sqlite3')
    rankingquery = db.cursor()
    sql = 'select distinct Age_Group_Performance, Age_Group_Performance as event2 '
    sql += 'from dataload_performances'
    sql += ' where club_at_performance LIKE "%Durham%"'
    rankingquery.execute(sql) 
    r = pd.DataFrame(rankingquery.fetchall(), columns = [x[0] for x in rankingquery.description])
    r = r.sort_values('Age_Group_Performance')
    r.loc[-1] = ['All','All']  # adding a row
    r.index = r.index + 1  # shifting index
    r =r.sort_index()
    event = tuple(r.itertuples(index=False, name=None))
    return event


Gender = [
        ('All',u'All'),     
        ('M',u'M'),
        ('W',u'W')
]

League = [('All','All'),('Northern Track & Field League North East Premier','Northern Track & Field League North East Premier'),
               ('Northern League - North East 1','Northern League - North East 1'),
               ('North East Youth Development League - Division 2','North East Youth Development League - Division 2'),
               ('North Eastern Youth Development League Division 2S','North Eastern Youth Development League Division 2S')
]
def League_Date():
    db = sqlite3.connect('db.sqlite3')
    rankingquery = db.cursor()
    sql = 'select distinct date, date as event2 '
    sql += 'from dataload_meets'
    rankingquery.execute(sql) 
    r = pd.DataFrame(rankingquery.fetchall(), columns = [x[0] for x in rankingquery.description])
    r = r.sort_values('date')
    r.loc[-1] = ['All','All']  # adding a row
    r.index = r.index + 1  # shifting index
    r = r.sort_index()
    event = tuple(r.itertuples(index=False, name=None))
    return event


ResultsView = [
        ('Best Performances',u'Best Performances'),
        ('Top 100 Performances',u'Top 100 Performances'),
        ('Total League Points',u'Total League Points'),
        ('League Tables',u'League Tables'),

]
class Results_Filter(forms.Form):
         # each field would be mapped as an input field in HTML
        Age_Group = forms.ChoiceField(choices=age_group())
        Event_Group = forms.ChoiceField(choices=event_group())
        Year = forms.ChoiceField(choices=year())
        Event = forms.ChoiceField(choices=event())
        Gender = forms.ChoiceField(choices=Gender)
        League = forms.ChoiceField(choices=League)
        League_Date = forms.ChoiceField(choices=League_Date)
        Results_View = forms.ChoiceField(choices=ResultsView)


