from django.db import models

# Create your models here.
class athlete(models.Model):
    firstname = models.CharField(max_length=50,default='') 
    surname = models.CharField(max_length=50,default='')
    track = models.CharField(max_length=50,default='')
    road = models.CharField(max_length=50,default='')
    xc = models.CharField(max_length=50,default='')
    sex = models.CharField(max_length=50,default='')
    club = models.CharField(max_length=50,default='')
    athlete_id = models.IntegerField()


class pbs(models.Model):
    athlete_id = models.ForeignKey(athlete, on_delete=models.CASCADE)
    event = models.CharField(max_length=50,default='')
    value = models.CharField(max_length=50,default='')
                        

class performances(models.Model):
    athlete_id = models.ForeignKey(athlete, on_delete=models.CASCADE)
    event = models.CharField(max_length=50,default='')
    value = models.CharField(max_length=50,default='')
    position = models.CharField(max_length=50,default='')
    raceid = models.CharField(max_length=50,default='')
    venue = models.CharField(max_length=50,default='')
    meeting = models.CharField(max_length=50,default='')
    date = models.CharField(max_length=50,default='')
                        

class ranks(models.Model):
    athlete_id = models.ForeignKey(athlete, on_delete=models.CASCADE)
    event = models.CharField(max_length=50,default='')
    age_group = models.CharField(max_length=50,default='')
    year = models.CharField(max_length=50,default='')
    rank = models.CharField(max_length=50,default='')
                        
class coaching(models.Model):
    athlete_id = models.ForeignKey(athlete, on_delete=models.CASCADE)
    name = models.CharField(max_length=50,default='')
    club = models.CharField(max_length=50,default='')
    age_group = models.CharField(max_length=50,default='')
    sex = models.CharField(max_length=50,default='')
    best_event = models.CharField(max_length=50,default='')
    rank = models.CharField(max_length=50,default='')
    age_group_rank = models.CharField(max_length=50,default='')
    year = models.CharField(max_length=50,default='')
    performance = models.CharField(max_length=50,default='')
