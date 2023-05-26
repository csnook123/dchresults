from django.shortcuts import render
from dataload.models import athlete, performances
from django.http import HttpResponse
from django.urls import reverse
import sqlite3
import pandas as pd