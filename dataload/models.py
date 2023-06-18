from django.db import models

# Create your models here.
class athlete(models.Model):
    firstname = models.CharField(max_length=50,default='') 
    surname = models.CharField(max_length=50,default='')
    name = models.CharField(max_length=50,default='')
    track = models.CharField(max_length=50,default='')
    road = models.CharField(max_length=50,default='')
    xc = models.CharField(max_length=50,default='')
    sex = models.CharField(max_length=50,default='')
    club = models.CharField(max_length=50,default='')
    athlete_id = models.CharField(max_length=50,default='')


class pbs(models.Model):
    athlete_id = models.CharField(max_length=50,default='')
    event = models.CharField(max_length=50,default='')
    value = models.CharField(max_length=50,default='')
                        

class performances(models.Model):
    athlete_id = models.CharField(max_length=50,default='')
    event = models.CharField(max_length=50,default='')
    performance = models.CharField(max_length=50,default='')
    position = models.CharField(max_length=50,default='')
    raceid = models.CharField(max_length=50,default='')
    venue = models.CharField(max_length=50,default='')
    meeting = models.CharField(max_length=50,default='')
    date = models.DateField(default='',null=False)
    club_at_performance = models.CharField(max_length=50,default='')
    Age_Group_Performance = models.CharField(max_length=50,default='')   
    event_group = models.CharField(max_length=50,default='')
    event_type = models.CharField(max_length=50,default='')
    year =  models.CharField(max_length=50,default='')
    XCSeason =  models.CharField(max_length=50,default='')

class ranks(models.Model):
    athlete_id = models.CharField(max_length=50,default='')
    event = models.CharField(max_length=50,default='')
    age_group = models.CharField(max_length=50,default='')
    year = models.CharField(max_length=50,default='')
    rank = models.CharField(max_length=50,default='')
                        
class coaching(models.Model):
    athlete_id = models.CharField(max_length=50,default='')
    name = models.CharField(max_length=50,default='')
    club = models.CharField(max_length=50,default='')
    age_group = models.CharField(max_length=50,default='')
    sex = models.CharField(max_length=50,default='')
    best_event = models.CharField(max_length=50,default='')
    rank = models.CharField(max_length=50,default='')
    age_group_rank = models.CharField(max_length=50,default='')
    year = models.CharField(max_length=50,default='')
    performance = models.CharField(max_length=50,default='')

class meets(models.Model):
    date = models.DateField(default='',null=False)
    meeting = models.CharField(max_length=50,default='')
    venue = models.CharField(max_length=50,default='')
    type = models.CharField(max_length=50,default='')
    meeting_id = models.CharField(max_length=50,default='')
    year =  models.CharField(max_length=50,default='')


class results(models.Model):
    meeting_id = models.CharField(max_length=50,default='')
    event = models.CharField(max_length=50,default='')
    event_age_group = models.CharField(max_length=50,default='')
    race = models.CharField(max_length=50,default='')
    pos = models.CharField(max_length=50,default='')
    perf = models.CharField(max_length=50,default='')
    name = models.CharField(max_length=50,default='')
    age_group = models.CharField(max_length=50,default='')
    gender = models.CharField(max_length=50,default='')
    club = models.CharField(max_length=50,default='')
    points = models.IntegerField(default=0)
    athlete_id = models.CharField(max_length=50,default='')
    event_group = models.CharField(max_length=50,default='')
    