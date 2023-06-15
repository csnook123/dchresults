# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


event_types = (
        ( 'Championships',u'Championships'),
        ('League',u'League'),
        ('Training',u'Training'),
        ('Other',u'Other'),
    )

age_group = (
        ('Junior', u'Junior'),
        ('Senior', u'Senior'),
        ('Masters', u'Masters'),
        ('All', u'All'),
    )


class Event(models.Model):
    day = models.DateField(u'Day of the event', help_text=u'Day of the event')
    start_time = models.TimeField(u'Starting time', help_text=u'Starting time')
    end_time = models.TimeField(u'Final time', help_text=u'Final time')    
    Category = models.CharField(max_length=32, choices=event_types, null=True, blank=True,help_text=u'Event Type')
    Age_Group = models.CharField(max_length=32, choices=age_group, null=True, blank=True,help_text=u'Age Groups')
    notes = models.TextField(u'Textual Notes', help_text=u'Textual Notes', blank=True, null=True)
 
    class Meta:
        verbose_name = u'Scheduling'
        verbose_name_plural = u'Scheduling'