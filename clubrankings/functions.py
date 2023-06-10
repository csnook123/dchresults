from django.shortcuts import render
from dataload.models import athlete, performances
from django.http import HttpResponse
from django.urls import reverse
import sqlite3
import pandas as pd

def event_type(event):
    #Function to Return if an event is:
    #Track and Field, Road Running, Cross Country, or Fell Running
    type_of_event = ''
    return type_of_event

def event_performance_sort_order(event):
    #Function to determine if performances should be sorted ascending or
    #descending for the top of the list to be the best performance
    sort_order = ''
    return sort_order

def event_group(event):
    #Function to allocate events to event groups for Track and Field
    #Categories to be used:
    ##Sprints and Hurdles,
    #Middle Distance and Endurance,
    #Relays
    #Throws
    #Jumps
    group = ''
    return group

def iaaf_scores(event, performance):
    #Function to calculate IAAF scores for relevant performances per the 2022 Tables
    #https://worldathletics.org/news/news/scoring-tables-2022
    score = 0
    return score

def event_scoring(variables):
    #Function to determine scores awarded for a particular event/league
    #Uses Race/Heat/other relevant information to determine scoring
    #Probably different for NAL, NEYDL and XC at least.
    #Potentially further events to score.
    score = 0
    return score

def db_conn_to_df(sql):
    #function to receive a sql statement and return it to a dataframe.
    dataframe =''
    return dataframe

