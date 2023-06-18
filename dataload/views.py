from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from .models import athlete,coaching,ranks,performances,pbs,meets,results
from django.http import HttpResponse
from timeit import default_timer
from datetime import datetime, timedelta
import sqlite3

# Create your views here.
initialslist = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

eventcategorisation = [
                        ('0.9MXC','Cross Country','Cross Country'),
                        ('1.16MNAD','Running - Various','Running - Various'),
                        ('1.1MNAD','Running - Various','Running - Various'),
                        ('1.25KXCL','Cross Country','Cross Country'),
                        ('1.25M','Running - Various','Running - Various'),
                        ('1.2KNAD','Running - Various','Running - Various'),
                        ('1.4M','Running - Various','Running - Various'),
                        ('1.5KMT','Running - Various','Running - Various'),
                        ('1.5KXC','Cross Country','Cross Country'),
                        ('1.5KXCL','Cross Country','Cross Country'),
                        ('1.5MXC','Cross Country','Cross Country'),
                        ('1.65KXCL','Cross Country','Cross Country'),
                        ('1.66ML','Running - Various','Running - Various'),
                        ('1.6KXCL','Cross Country','Cross Country'),
                        ('1.6MNAD','Running - Various','Running - Various'),
                        ('1.7ML','Running - Various','Running - Various'),
                        ('1.8KXCL','Cross Country','Cross Country'),
                        ('1.8M','Running - Various','Running - Various'),
                        ('1.8ML','Running - Various','Running - Various'),
                        ('1.8MXC','Cross Country','Cross Country'),
                        ('1.8MXCL','Cross Country','Cross Country'),
                        ('1.91ML','Running - Various','Running - Various'),
                        ('1.9KNAD','Running - Various','Running - Various'),
                        ('10.22KXC','Cross Country','Cross Country'),
                        ('10.2KXC','Cross Country','Cross Country'),
                        ('10.3KXC','Cross Country','Cross Country'),
                        ('10.4KXC','Cross Country','Cross Country'),
                        ('10.5K','Running - Various','Running - Various'),
                        ('10.5KXC','Cross Country','Cross Country'),
                        ('10.6KXC','Cross Country','Cross Country'),
                        ('10.7K','Running - Various','Running - Various'),
                        ('10.8KXC','Cross Country','Cross Country'),
                        ('100','Track and Field','Sprints'),
                        ('1000','Track and Field','Endurance'),
                        ('10000','Track and Field','Endurance'),
                        ('100000','Running - Various','Running - Various'),
                        ('100HU17M','Track and Field','Barriers'),
                        ('100HW','Track and Field','Barriers'),
                        ('100K','Running - Various','Running - Various'),
                        ('100Miles','Running - Various','Running - Various'),
                        ('10K','Running - Standard','Running - Standard'),
                        ('10KL','Running - Various','Running - Various'),
                        ('10KMT','Running - Various','Running - Various'),
                        ('10KNAD','Running - Various','Running - Various'),
                        ('10KXC','Cross Country','Cross Country'),
                        ('10KXCL','Cross Country','Cross Country'),
                        ('10M','Running - Various','Running - Various'),
                        ('10MMT','Running - Various','Running - Various'),
                        ('11.1KXC','Cross Country','Cross Country'),
                        ('11.2KXC','Cross Country','Cross Country'),
                        ('11.5KMT','Running - Various','Running - Various'),
                        ('11.5KXC','Cross Country','Cross Country'),
                        ('11.8KXC','Cross Country','Cross Country'),
                        ('110','Running - Various','Running - Various'),
                        ('110H','Track and Field','Barriers'),
                        ('110HC','Track and Field','Barriers'),
                        ('110HU20M','Track and Field','Barriers'),
                        ('11KMT','Running - Various','Running - Various'),
                        ('11KXC','Cross Country','Cross Country'),
                        ('12.1KXC','Cross Country','Cross Country'),
                        ('12.3KXC','Cross Country','Cross Country'),
                        ('12.5K','Running - Various','Running - Various'),
                        ('12.5KMT','Running - Various','Running - Various'),
                        ('12.9KXC','Cross Country','Cross Country'),
                        ('1200','Track and Field','Endurance'),
                        ('12KMT','Running - Various','Running - Various'),
                        ('12KXC','Cross Country','Cross Country'),
                        ('12hours','Running - Various','Running - Various'),
                        ('13.5KXC','Cross Country','Cross Country'),
                        ('13.83M','Running - Various','Running - Various'),
                        ('14.188M','Running - Various','Running - Various'),
                        ('14K','Running - Various','Running - Various'),
                        ('14M','Running - Various','Running - Various'),
                        ('14MMT','Running - Various','Running - Various'),
                        ('150','Track and Field','Sprints'),
                        ('1500','Track and Field','Endurance'),
                        ('1500SC','Track and Field','Barriers'),
                        ('1500SCW','Track and Field','Barriers'),
                        ('15K','Running - Various','Running - Various'),
                        ('15KMT','Running - Various','Running - Various'),
                        ('15KXC','Cross Country','Cross Country'),
                        ('15M','Running - Various','Running - Various'),
                        ('1K','Running - Various','Running - Various'),
                        ('1KNAD','Running - Various','Running - Various'),
                        ('1KXC','Cross Country','Cross Country'),
                        ('1M','Running - Various','Running - Various'),
                        ('1ML','Running - Various','Running - Various'),
                        ('1MMT','Running - Various','Running - Various'),
                        ('1MNAD','Running - Various','Running - Various'),
                        ('1MXC','Cross Country','Cross Country'),
                        ('2.1MXC','Cross Country','Cross Country'),
                        ('2.22ML','Running - Various','Running - Various'),
                        ('2.28M','Running - Various','Running - Various'),
                        ('2.291KL','Running - Various','Running - Various'),
                        ('2.2KNAD','Running - Various','Running - Various'),
                        ('2.2KXC','Cross Country','Cross Country'),
                        ('2.2ML','Running - Various','Running - Various'),
                        ('2.2MXC','Cross Country','Cross Country'),
                        ('2.3K','Running - Various','Running - Various'),
                        ('2.3KNAD','Running - Various','Running - Various'),
                        ('2.3KXC','Cross Country','Cross Country'),
                        ('2.3KXCL','Cross Country','Cross Country'),
                        ('2.43KXC','Cross Country','Cross Country'),
                        ('2.45KXC','Cross Country','Cross Country'),
                        ('2.4KXC','Cross Country','Cross Country'),
                        ('2.59KXC','Cross Country','Cross Country'),
                        ('2.5K','Running - Various','Running - Various'),
                        ('2.5KMT','Running - Various','Running - Various'),
                        ('2.5KNAD','Running - Various','Running - Various'),
                        ('2.5KXC','Cross Country','Cross Country'),
                        ('2.5KXCL','Cross Country','Cross Country'),
                        ('2.5MMTL','Running - Various','Running - Various'),
                        ('2.6K','Running - Various','Running - Various'),
                        ('2.6KXC','Cross Country','Cross Country'),
                        ('2.75KXC','Cross Country','Cross Country'),
                        ('2.75MMTL','Running - Various','Running - Various'),
                        ('2.7ML','Running - Various','Running - Various'),
                        ('2.8KXC','Cross Country','Cross Country'),
                        ('2.997KL','Running - Various','Running - Various'),
                        ('2.9KXC','Cross Country','Cross Country'),
                        ('200','Track and Field','Sprints'),
                        ('2000','Track and Field','Endurance'),
                        ('200000','Running - Various','Running - Various'),
                        ('2000SC','Track and Field','Barriers'),
                        ('2000SCW','Track and Field','Barriers'),
                        ('2000W','Track and Field','Endurance'),
                        ('20K','Track and Field','Endurance'),
                        ('20KMT','Track and Field','Endurance'),
                        ('20M','Running - Various','Running - Various'),
                        ('20MMT','Running - Various','Running - Various'),
                        ('20MNAD','Running - Various','Running - Various'),
                        ('21.5KNAD','Running - Various','Running - Various'),
                        ('215MMT','Running - Various','Running - Various'),
                        ('24 Hours','Running - Various','Running - Various'),
                        ('24H','Running - Various','Running - Various'),
                        ('24Hours','Running - Various','Running - Various'),
                        ('24hours','Running - Various','Running - Various'),
                        ('2KMT','Running - Various','Running - Various'),
                        ('2KNAD','Running - Various','Running - Various'),
                        ('2KXCL','Cross Country','Cross Country'),
                        ('2M','Running - Various','Running - Various'),
                        ('2ML','Running - Various','Running - Various'),
                        ('2MNAD','Running - Various','Running - Various'),
                        ('2MXC','Cross Country','Cross Country'),
                        ('2MXCL','Cross Country','Cross Country'),
                        ('2Miles','Running - Various','Running - Various'),
                        ('3.01KXCL','Cross Country','Cross Country'),
                        ('3.03ML','Running - Various','Running - Various'),
                        ('3.05KXC','Cross Country','Cross Country'),
                        ('3.09KXC','Cross Country','Cross Country'),
                        ('3.13KXC','Cross Country','Cross Country'),
                        ('3.19KXC','Cross Country','Cross Country'),
                        ('3.1KL','Running - Various','Running - Various'),
                        ('3.1KXC','Cross Country','Cross Country'),
                        ('3.1ML','Running - Various','Running - Various'),
                        ('3.2KL','Running - Various','Running - Various'),
                        ('3.2KXC','Cross Country','Cross Country'),
                        ('3.35KXC','Cross Country','Cross Country'),
                        ('3.3KXC','Cross Country','Cross Country'),
                        ('3.41M','Running - Various','Running - Various'),
                        ('3.4MXC','Cross Country','Cross Country'),
                        ('3.5KL','Running - Various','Running - Various'),
                        ('3.5KMR','Running - Various','Running - Various'),
                        ('3.5KXC','Cross Country','Cross Country'),
                        ('3.5MMT','Running - Various','Running - Various'),
                        ('3.5MXC','Cross Country','Cross Country'),
                        ('3.6KXC','Cross Country','Cross Country'),
                        ('3.75KXC','Cross Country','Cross Country'),
                        ('3.75MMT','Running - Various','Running - Various'),
                        ('3.75MNAD','Running - Various','Running - Various'),
                        ('3.7KL','Running - Various','Running - Various'),
                        ('3.7KXC','Cross Country','Cross Country'),
                        ('3.83KXC','Cross Country','Cross Country'),
                        ('3.851KL','Running - Various','Running - Various'),
                        ('3.861KL','Running - Various','Running - Various'),
                        ('3.863KL','Running - Various','Running - Various'),
                        ('3.88KL','Running - Various','Running - Various'),
                        ('3.8KXC','Cross Country','Cross Country'),
                        ('3.8M','Running - Various','Running - Various'),
                        ('3.8ML','Running - Various','Running - Various'),
                        ('3.8MMT','Running - Various','Running - Various'),
                        ('3.8MXC','Cross Country','Cross Country'),
                        ('3.9KXC','Cross Country','Cross Country'),
                        ('3.9M','Running - Various','Running - Various'),
                        ('300','Track and Field','Sprints'),
                        ('3000','Track and Field','Endurance'),
                        ('3000SC','Track and Field','Barriers'),
                        ('300HW','Track and Field','Barriers'),
                        ('30K','Running - Various','Running - Various'),
                        ('3K','Running - Various','Running - Various'),
                        ('3KL','Running - Various','Running - Various'),
                        ('3KMT','Running - Various','Running - Various'),
                        ('3KNAD','Running - Various','Running - Various'),
                        ('3KXC','Cross Country','Cross Country'),
                        ('3KXCL','Cross Country','Cross Country'),
                        ('3M','Running - Various','Running - Various'),
                        ('3ML','Running - Various','Running - Various'),
                        ('3MMT','Running - Various','Running - Various'),
                        ('3MXC','Cross Country','Cross Country'),
                        ('4.175KXC','Cross Country','Cross Country'),
                        ('4.17KXC','Cross Country','Cross Country'),
                        ('4.1KMR','Running - Various','Running - Various'),
                        ('4.1KXC','Cross Country','Cross Country'),
                        ('4.22KXC','Cross Country','Cross Country'),
                        ('4.23M','Running - Various','Running - Various'),
                        ('4.245KXC','Cross Country','Cross Country'),
                        ('4.25M','Running - Various','Running - Various'),
                        ('4.25MMT','Running - Various','Running - Various'),
                        ('4.2KMR','Running - Various','Running - Various'),
                        ('4.2KXC','Cross Country','Cross Country'),
                        ('4.2MMT','Running - Various','Running - Various'),
                        ('4.2MXC','Cross Country','Cross Country'),
                        ('4.315KL','Running - Various','Running - Various'),
                        ('4.33KL','Running - Various','Running - Various'),
                        ('4.35KXC','Cross Country','Cross Country'),
                        ('4.395KXC','Cross Country','Cross Country'),
                        ('4.39KXC','Cross Country','Cross Country'),
                        ('4.3KXC','Cross Country','Cross Country'),
                        ('4.4KXC','Cross Country','Cross Country'),
                        ('4.4MXC','Cross Country','Cross Country'),
                        ('4.5KL','Running - Various','Running - Various'),
                        ('4.5KXC','Cross Country','Cross Country'),
                        ('4.5ML','Running - Various','Running - Various'),
                        ('4.5MMT','Running - Various','Running - Various'),
                        ('4.5MXC','Cross Country','Cross Country'),
                        ('4.6KXC','Cross Country','Cross Country'),
                        ('4.6ML','Running - Various','Running - Various'),
                        ('4.6MXC','Cross Country','Cross Country'),
                        ('4.7KXC','Cross Country','Cross Country'),
                        ('4.7MMT','Running - Various','Running - Various'),
                        ('4.7MXC','Cross Country','Cross Country'),
                        ('4.819KL','Running - Various','Running - Various'),
                        ('4.8KL','Running - Various','Running - Various'),
                        ('4.8KXC','Cross Country','Cross Country'),
                        ('4.8M','Running - Various','Running - Various'),
                        ('4.8ML','Running - Various','Running - Various'),
                        ('4.8MMT','Running - Various','Running - Various'),
                        ('4.99KXC','Cross Country','Cross Country'),
                        ('4.9KL','Running - Various','Running - Various'),
                        ('4.9KXC','Cross Country','Cross Country'),
                        ('400','Track and Field','Sprints'),
                        ('400H','Track and Field','Barriers'),
                        ('400HU17M','Track and Field','Barriers'),
                        ('400HW','Track and Field','Barriers'),
                        ('4K','Running - Various','Running - Various'),
                        ('4KL','Running - Various','Running - Various'),
                        ('4KNAD','Running - Various','Running - Various'),
                        ('4KXC','Cross Country','Cross Country'),
                        ('4KXCL','Cross Country','Cross Country'),
                        ('4KXL','Running - Various','Running - Various'),
                        ('4M','Running - Various','Running - Various'),
                        ('4MMT','Running - Various','Running - Various'),
                        ('4MNAD','Running - Various','Running - Various'),
                        ('4MXC','Cross Country','Cross Country'),
                        ('4X100','Track and Field','Relays'),
                        ('4x100','Track and Field','Relays'),
                        ('4x200','Track and Field','Relays'),
                        ('4x400','Track and Field','Relays'),
                        ('5.03KXC','Cross Country','Cross Country'),
                        ('5.053KL','Running - Various','Running - Various'),
                        ('5.08KL','Running - Various','Running - Various'),
                        ('5.14KL','Running - Various','Running - Various'),
                        ('5.1KXC','Cross Country','Cross Country'),
                        ('5.1MMT','Running - Various','Running - Various'),
                        ('5.22KXC','Cross Country','Cross Country'),
                        ('5.25MXC','Cross Country','Cross Country'),
                        ('5.2KL','Running - Various','Running - Various'),
                        ('5.2KNAD','Running - Various','Running - Various'),
                        ('5.2KXC','Cross Country','Cross Country'),
                        ('5.2M','Running - Various','Running - Various'),
                        ('5.2MMT','Running - Various','Running - Various'),
                        ('5.32MMT','Running - Various','Running - Various'),
                        ('5.3KXC','Cross Country','Cross Country'),
                        ('5.4KXC','Cross Country','Cross Country'),
                        ('5.4M','Running - Various','Running - Various'),
                        ('5.4MMT','Running - Various','Running - Various'),
                        ('5.4MXC','Cross Country','Cross Country'),
                        ('5.54ML','Running - Various','Running - Various'),
                        ('5.5KXC','Cross Country','Cross Country'),
                        ('5.5MMT','Running - Various','Running - Various'),
                        ('5.65KXC','Cross Country','Cross Country'),
                        ('5.67M','Running - Various','Running - Various'),
                        ('5.68KXC','Cross Country','Cross Country'),
                        ('5.68MXC','Cross Country','Cross Country'),
                        ('5.6KL','Running - Various','Running - Various'),
                        ('5.6KXC','Cross Country','Cross Country'),
                        ('5.75KXC','Cross Country','Cross Country'),
                        ('5.7KXC','Cross Country','Cross Country'),
                        ('5.7M','Running - Various','Running - Various'),
                        ('5.7MMT','Running - Various','Running - Various'),
                        ('5.848KL','Running - Various','Running - Various'),
                        ('5.85KXC','Cross Country','Cross Country'),
                        ('5.88KL','Running - Various','Running - Various'),
                        ('5.8KXC','Cross Country','Cross Country'),
                        ('5.8ML','Running - Various','Running - Various'),
                        ('5.994KL','Running - Various','Running - Various'),
                        ('5.9KXC','Cross Country','Cross Country'),
                        ('5.9M','Running - Various','Running - Various'),
                        ('50','Running - Various','Running - Various'),
                        ('5000','Track and Field','Endurance'),
                        ('50000','Running - Various','Running - Various'),
                        ('50K','Running - Various','Running - Various'),
                        ('50KMT','Running - Various','Running - Various'),
                        ('50Miles','Running - Various','Running - Various'),
                        ('53MMT','Running - Various','Running - Various'),
                        ('5K','Running - Various','Running - Various'),
                        ('5KDH','Running - Various','Running - Various'),
                        ('5KL','Running - Various','Running - Various'),
                        ('5KMT','Running - Various','Running - Various'),
                        ('5KNAD','Running - Various','Running - Various'),
                        ('5KXC','Cross Country','Cross Country'),
                        ('5KXCL','Cross Country','Cross Country'),
                        ('5M','Running - Various','Running - Various'),
                        ('5MMT','Running - Various','Running - Various'),
                        ('5MNAD','Running - Various','Running - Various'),
                        ('5MXC','Cross Country','Cross Country'),
                        ('6.09KXC','Cross Country','Cross Country'),
                        ('6.1KXC','Cross Country','Cross Country'),
                        ('6.1MMT','Running - Various','Running - Various'),
                        ('6.2KXC','Cross Country','Cross Country'),
                        ('6.2M','Running - Various','Running - Various'),
                        ('6.2MMT','Running - Various','Running - Various'),
                        ('6.3KXC','Cross Country','Cross Country'),
                        ('6.3MXC','Cross Country','Cross Country'),
                        ('6.4KL','Running - Various','Running - Various'),
                        ('6.4KXC','Cross Country','Cross Country'),
                        ('6.4M','Running - Various','Running - Various'),
                        ('6.4MMT','Running - Various','Running - Various'),
                        ('6.53KXC','Cross Country','Cross Country'),
                        ('6.5KL','Running - Various','Running - Various'),
                        ('6.5KXC','Cross Country','Cross Country'),
                        ('6.5M','Running - Various','Running - Various'),
                        ('6.5MMT','Running - Various','Running - Various'),
                        ('6.5MXC','Cross Country','Cross Country'),
                        ('6.6KXC','Cross Country','Cross Country'),
                        ('6.6MXC','Cross Country','Cross Country'),
                        ('6.7KXC','Cross Country','Cross Country'),
                        ('6.7MMT','Running - Various','Running - Various'),
                        ('6.8KL','Running - Various','Running - Various'),
                        ('6.8KXC','Cross Country','Cross Country'),
                        ('6.8M','Running - Various','Running - Various'),
                        ('6.97KXC','Cross Country','Cross Country'),
                        ('6.995KXC','Cross Country','Cross Country'),
                        ('60','Track and Field','Sprints'),
                        ('600','Track and Field','Endurance'),
                        ('60H','Track and Field','Barriers'),
                        ('60HU13M','Track and Field','Barriers'),
                        ('60HU13W','Track and Field','Barriers'),
                        ('60HU15M','Track and Field','Barriers'),
                        ('60HU15W','Track and Field','Barriers'),
                        ('60HU17W','Track and Field','Barriers'),
                        ('60HU20M','Track and Field','Barriers'),
                        ('60HW','Track and Field','Barriers'),
                        ('6H','Running - Various','Running - Various'),
                        ('6Hours','Running - Various','Running - Various'),
                        ('6K','Running - Various','Running - Various'),
                        ('6KL','Running - Various','Running - Various'),
                        ('6KXC','Cross Country','Cross Country'),
                        ('6KXCL','Cross Country','Cross Country'),
                        ('6M','Running - Various','Running - Various'),
                        ('6MMT','Running - Various','Running - Various'),
                        ('6MNAD','Running - Various','Running - Various'),
                        ('6MXC','Cross Country','Cross Country'),
                        ('7.1KXC','Cross Country','Cross Country'),
                        ('7.2KXC','Cross Country','Cross Country'),
                        ('7.38KXC','Cross Country','Cross Country'),
                        ('7.3KXC','Cross Country','Cross Country'),
                        ('7.47KXC','Cross Country','Cross Country'),
                        ('7.4KXC','Cross Country','Cross Country'),
                        ('7.5KXC','Cross Country','Cross Country'),
                        ('7.5MMT','Running - Various','Running - Various'),
                        ('7.7KXC','Cross Country','Cross Country'),
                        ('7.7MMT','Running - Various','Running - Various'),
                        ('7.8KXC','Cross Country','Cross Country'),
                        ('7.9KXC','Cross Country','Cross Country'),
                        ('7.9MNAD','Running - Various','Running - Various'),
                        ('70HU13W','Track and Field','Barriers'),
                        ('75','Track and Field','Sprints'),
                        ('75HU13M','Track and Field','Barriers'),
                        ('75HU15M','Track and Field','Barriers'),
                        ('75HU15W','Track and Field','Barriers'),
                        ('77KMT','Running - Various','Running - Various'),
                        ('78K','Running - Various','Running - Various'),
                        ('7H','Running - Various','Running - Various'),
                        ('7KXC','Cross Country','Cross Country'),
                        ('7M','Running - Various','Running - Various'),
                        ('7MMT','Running - Various','Running - Various'),
                        ('7MNAD','Running - Various','Running - Various'),
                        ('8.05KXC','Cross Country','Cross Country'),
                        ('8.18KXC','Cross Country','Cross Country'),
                        ('8.1KXC','Cross Country','Cross Country'),
                        ('8.1MMT','Running - Various','Running - Various'),
                        ('8.25KXC','Cross Country','Cross Country'),
                        ('8.2KXC','Cross Country','Cross Country'),
                        ('8.3KXC','Cross Country','Cross Country'),
                        ('8.4KXC','Cross Country','Cross Country'),
                        ('8.4MMT','Running - Various','Running - Various'),
                        ('8.5KL','Running - Various','Running - Various'),
                        ('8.5KXC','Cross Country','Cross Country'),
                        ('8.662KL','Running - Various','Running - Various'),
                        ('8.6KXC','Cross Country','Cross Country'),
                        ('8.74M','Running - Various','Running - Various'),
                        ('8.9KXC','Cross Country','Cross Country'),
                        ('80','Track and Field','Sprints'),
                        ('800','Track and Field','Endurance'),
                        ('80HU15M','Track and Field','Barriers'),
                        ('80HU17W','Track and Field','Barriers'),
                        ('85KMT','Running - Various','Running - Various'),
                        ('87.7K','Running - Various','Running - Various'),
                        ('87K','Running - Various','Running - Various'),
                        ('89K','Running - Various','Running - Various'),
                        ('8KXC','Cross Country','Cross Country'),
                        ('8M','Running - Various','Running - Various'),
                        ('8MMT','Running - Various','Running - Various'),
                        ('9.05KXC','Cross Country','Cross Country'),
                        ('9.15KXC','Cross Country','Cross Country'),
                        ('9.1KXC','Cross Country','Cross Country'),
                        ('9.2KXC','Cross Country','Cross Country'),
                        ('9.3MMT','Running - Various','Running - Various'),
                        ('9.5KXC','Cross Country','Cross Country'),
                        ('9.62KXC','Cross Country','Cross Country'),
                        ('9.65KXC','Cross Country','Cross Country'),
                        ('9.6KXC','Cross Country','Cross Country'),
                        ('9.7KXC','Cross Country','Cross Country'),
                        ('9.84KXC','Cross Country','Cross Country'),
                        ('9.8KXC','Cross Country','Cross Country'),
                        ('90','Running - Various','Running - Various'),
                        ('90.184K','Running - Various','Running - Various'),
                        ('9K','Running - Various','Running - Various'),
                        ('9KMT','Running - Various','Running - Various'),
                        ('9KXC','Cross Country','Cross Country'),
                        ('9MNAD','Running - Various','Running - Various'),
                        ('DT0.75K','Track and Field','Throws'),
                        ('DT1.25K','Track and Field','Throws'),
                        ('DT1.5K','Track and Field','Throws'),
                        ('DT1.75K','Track and Field','Throws'),
                        ('DT1K','Track and Field','Throws'),
                        ('DT2K','Track and Field','Throws'),
                        ('DecU17M','Track and Field','Combined Events'),
                        ('DecU20M','Track and Field','Combined Events'),
                        ('HJ','Track and Field','Jumps'),
                        ('HM','Running - Standard','Running - Standard'),
                        ('HMDH','Running - Various','Running - Various'),
                        ('HMMT','Running - Various','Running - Various'),
                        ('HMNAD','Running - Various','Running - Various'),
                        ('HT4K','Track and Field','Throws'),
                        ('HT5K','Track and Field','Throws'),
                        ('HT6K','Track and Field','Throws'),
                        ('HT7.26K','Track and Field','Throws'),
                        ('HepIU17W','Track and Field','Combined Events'),
                        ('HepU17W','Track and Field','Combined Events'),
                        ('HepW','Track and Field','Combined Events'),
                        ('JT400','Track and Field','Throws'),
                        ('JT500','Track and Field','Throws'),
                        ('JT600','Track and Field','Throws'),
                        ('JT700','Track and Field','Throws'),
                        ('JT800','Track and Field','Throws'),
                        ('LJ','Track and Field','Jumps'),
                        ('Mar','Running - Standard','Running - Standard'),
                        ('MarDH','Running - Various','Running - Various'),
                        ('MarMT','Running - Various','Running - Various'),
                        ('Mile','Track and Field','Endurance'),
                        ('OctU17M','Track and Field','Combined Events'),
                        ('PV','Track and Field','Jumps'),
                        ('Pen','Track and Field','Combined Events'),
                        ('PenI','Track and Field','Combined Events'),
                        ('PenINSU17W','Track and Field','Combined Events'),
                        ('PenIU13MNS','Track and Field','Combined Events'),
                        ('PenIU13WNS','Track and Field','Combined Events'),
                        ('PenIU15MNS','Track and Field','Combined Events'),
                        ('PenIU17W','Track and Field','Combined Events'),
                        ('PenIU17WNS','Track and Field','Combined Events'),
                        ('PenIW','Track and Field','Combined Events'),
                        ('PenM45','Track and Field','Combined Events'),
                        ('PenNSM45','Track and Field','Combined Events'),
                        ('PenNSU13W','Track and Field','Combined Events'),
                        ('PenNSU20M','Track and Field','Combined Events'),
                        ('PenU13M','Track and Field','Combined Events'),
                        ('PenU13W','Track and Field','Combined Events'),
                        ('PenU15M','Track and Field','Combined Events'),
                        ('PenU15W','Track and Field','Combined Events'),
                        ('PenU15WNS','Track and Field','Combined Events'),
                        ('PenU17M','Track and Field','Combined Events'),
                        ('PenU17W','Track and Field','Combined Events'),
                        ('PenW','Track and Field','Combined Events'),
                        ('PenW45NS','Track and Field','Combined Events'),
                        ('QM','Running - Various','Running - Various'),
                        ('RELAY','Running - Various','Running - Various'),
                        ('SHORT10K','Running - Various','Running - Various'),
                        ('SHORT10KMT','Running - Various','Running - Various'),
                        ('SHORT10M','Running - Various','Running - Various'),
                        ('SHORT5K','Running - Various','Running - Various'),
                        ('SHORT5KMT','Running - Various','Running - Various'),
                        ('SHORT5M','Running - Various','Running - Various'),
                        ('SHORTHM','Running - Various','Running - Various'),
                        ('SHORTMar','Running - Various','Running - Various'),
                        ('SHORTparkrun','Running - Various','Running - Various'),
                        ('SP2.72K','Track and Field','Throws'),
                        ('SP2K','Track and Field','Throws'),
                        ('SP3.25K','Track and Field','Throws'),
                        ('SP3K','Track and Field','Throws'),
                        ('SP4K','Track and Field','Throws'),
                        ('SP5K','Track and Field','Throws'),
                        ('SP6K','Track and Field','Throws'),
                        ('SP7.26K','Track and Field','Throws'),
                        ('TJ','Track and Field','Jumps'),
                        ('WT15.88K','Track and Field','Throws'),
                        ('ZFL','Running - Various','Running - Various'),
                        ('ZFLL','Running - Various','Running - Various'),
                        ('ZMR','Running - Various','Running - Various'),
                        ('ZMT','Running - Various','Running - Various'),
                        ('ZMTL','Running - Various','Running - Various'),
                        ('ZRD','Running - Various','Running - Various'),
                        ('ZRDL','Running - Various','Running - Various'),
                        ('ZRL','Running - Various','Running - Various'),
                        ('ZXC','Cross Country','Cross Country'),
                        ('ZXCL','Cross Country','Cross Country'),
                        ('parkrun','Running - Standard','Running - Standard'),
                        ('All','All','All'),

]


def geteventgroup(event):
    for item in eventcategorisation: 
        if item[0] == event:
            evgroup = item[2]
    return evgroup

def geteventtype(event):
    for item in eventcategorisation: 
        if item[0] == event:
            evtype = item[1]
    return evtype


def league_points_calc(heat,position):
        r=0
        if position == "1": r = 9 
        if position == "2": r = 7 
        if position == "3": r = 6 
        if position == "4": r = 5 
        if position == "5": r = 4 
        if position == "6": r = 3 
        if heat == "B" and r != 0: r = r-2
        if heat == 'nsA': r =0
        return  r


def loadalldata(request):
    start = default_timer()
    loadathletes()
    performanceload()
    coachingload()
    personalbests()
    rankingsload()
    end = default_timer()
    return HttpResponse('All Data loaded  '  + repr(end-start))

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
                            name = row[0].text + ' ' + row[1].text,
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
            b = getattr(i,'athlete_id')
            urlathlete = f'https://www.thepowerof10.info/athletes/profile.aspx?athleteid='
            urlathlete += f'{b}'
            htmlathlete = requests.get(urlathlete)
            soupathlete = BeautifulSoup(htmlathlete.text, 'html.parser')                
            coach_dets = soupathlete.find('div', {'id': 'cphBody_pnlAthletesCoached'})
            if  coach_dets is not None:
                s = coach_dets.find('table', {'class': 'alternatingrowspanel'}).find_all('tr')
                for n in s:
                    dets = n.find_all('td')
                    if dets[0].text != 'Name':
                        coach = coaching(
                            athlete_id = b,
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
            b = getattr(i,'athlete_id')
            urlathlete = f'https://www.thepowerof10.info/athletes/profile.aspx?athleteid='
            urlathlete += f'{b}'
            htmlathlete = requests.get(urlathlete)
            soupathlete = BeautifulSoup(htmlathlete.text, 'html.parser')                
            athlete_pb = soupathlete.find('div', {'id': 'cphBody_divBestPerformances'}).find_all('tr')
            for n in athlete_pb:
                if n.find('b').text != 'Event':
                    pb = pbs(
                        athlete_id = b,
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
  #      try:
            b = getattr(i,'athlete_id')
            urlathlete = f'https://www.thepowerof10.info/athletes/profile.aspx?athleteid='
            urlathlete += f'{b}'
            htmlathlete = requests.get(urlathlete)
            soupathlete = BeautifulSoup(htmlathlete.text, 'html.parser')                
            athlete_perf = soupathlete.find('div', {'id': 'cphBody_pnlPerformances'}).find_all('table')[1].find_all('tr')
            for n in athlete_perf:
                if len(n.find_all('td')) == 1:
                    dets = n.find_all('td')
                    clubs = dets[0].text
                    agp = clubs[5:8:1]
                    if clubs[9:15:1] == 'Durham':
                        check = 'Durham'
                    else: check = 'Not Durham'    
                if len(n.find_all('td')) > 1 and 'EventPerfPosVenueMeetingDate' != n.text:
                    dets = n.find_all('td')
                    dateformatting = dets[11].text
                    dateformatting = datetime.strptime(dateformatting, "%d %b %y")
                    xcdate = dateformatting - timedelta(180)
                    yr1 = dateformatting.year
                    xcdate = xcdate.year
                    perf = performances(
                        athlete_id = b,
                        event = dets[0].text,
                        performance = dets[1].text,
                        position = dets[5].text,
                        raceid = dets[6].text,
                        venue = dets[9].text,
                        meeting = dets[10].text,
                        date = dateformatting,
                        club_at_performance = check,
                        Age_Group_Performance = agp,
                        event_group = geteventgroup(dets[0].text),
                        event_type = geteventgroup(dets[0].text),
                        year = yr1,
                        XCSeason = xcdate
                    )
                    perf.save()
 #       except:
 #           ''
    end = default_timer()
    return HttpResponse('Performances Saved time taken' + repr(end-start))

def rankingsload(request):
    start = default_timer()
    a = ranks.objects.all()
    a.delete()
    for i in athlete.objects.all():
        try: 
            b = getattr(i,'athlete_id')
            urlathlete = f'https://www.thepowerof10.info/athletes/profile.aspx?athleteid='
            urlathlete += f'{b}'
            htmlathlete = requests.get(urlathlete)
            soupathlete = BeautifulSoup(htmlathlete.text, 'html.parser')                
            athlete_rank = soupathlete.find('div', {'id': 'cphBody_pnlMain'}).find('td', {'width': 220, 'valign': 'top'}).find_all('table')
            if len(athlete_rank) > 2:
                for n in athlete_rank[2].find_all('tr'):
                    dets = n.find_all('td')
                    if dets[0].text != 'Event':
                        rankings = ranks(
                            athlete_id = b,
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

    iterator.execute('select * from dataload_meets')
    f = 0
    for i in iterator.fetchall():
        f = f+1

    iterator.execute('select * from dataload_results')
    g = 0
    for i in iterator.fetchall():
        g = g+1

    links = '<br><a href=loadathletes>Load Athletes</a>'
    links += '<br><a href=coachingload>Load Coaching Records</a>'
    links += '<br><a href=performanceload>Load Performances</a>'
    links += '<br><a href=personalbests>Load PBs</a>'
    links += '<br><a href=events_load>Load Meets</a>'
    links += '<br><a href=events_results_load>Load Results</a>'
    links += '<br><a href=rankings>Load Rankings</a>'
    

    return HttpResponse('Athletes Loaded ' + str(a) +'<br>Coaching Records Loaded ' 
                        + str(b) + '<br>Rankings Loaded ' + str(c) + '<br>Performances Loaded '
                        + str(d) + '<br>PBs Loaded ' + str(e)+ '<br>Meets Loaded ' + str(f)
                        + '<br>Results Loaded ' + str(g) + links)


def events_load(request):
    meetings =['Northern Track %26 Field League North East Premier',
               'Northern League - North East 1',
               'North East Youth Development League - Division 2',
               'North Eastern Youth Development League Division 2S']

#meeting=None, venue=None, date_from=None, year=None, date_to=None, meeting_type=None, terrain=None):

    start = default_timer()
    a = meets.objects.all()
    a.delete()
    
    for x in meetings:
        url = 'https://www.thepowerof10.info/results/resultslookup.aspx?'
        m = str(x)
        url += f'title={m.replace(" ","+")}&'
        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'html.parser')

        try:
            table = soup.find('table', {'id': 'cphBody_dgMeetings'}).find_all('tr')
        except Exception as e:
            ''
        for i in table:
            dets = i.find_all('td')
            if dets[0].text != 'Date':
                dateformatting = dets[0].text
                dateformatting = dateformatting[4:len(dets[0].text):1]
                dateformatting = datetime.strptime(dateformatting, "%d %b %Y")
                yr = dateformatting.year
                n = meets(
                        date = dateformatting,
                        meeting = dets[1].text.replace('\n','').replace('\r','').replace('     ','').replace('Info',''),
                        venue = dets[2].text,
                        type = dets[3].text,
                        meeting_id = str(dets[2]).split('"')[1].split('=')[1],
                        year = yr
                    )
                n.save()
    end = default_timer()
    return HttpResponse('Meet Loaded ' + repr(end-start))

def event_results_load(request):
    a = results.objects.all()
    a.delete()
    start = default_timer()
    a = meets.objects.all()

    for competitions in a:
        j = competitions.meeting_id
        for pageno in [1,2,3]:
            try: 
                url = f'https://www.thepowerof10.info/results/results.aspx?meetingid={j}&pagenum={pageno}'
                html = requests.get(url)
                soup = BeautifulSoup(html.text, 'html.parser')
                meeting_dets = soup.find('div', {'id': 'pnlMainGeneral'}).find_all('table')[0].find('span')
                meeting_res = soup.find('table', {'id': 'cphBody_dgP'}).find_all('tr')[1:]
                count = -1
                for i in meeting_res:
                    dets = i.find_all('td')
                    if len(dets) == 1 and '\xa0' not in str(dets[0]):
                        vals = str(dets[0].text).split(" ")
                        count += 1    
                    else:
                        if '\xa0' not in str(dets[0]) and 'Pos' not in str(dets[0].text) :
                            #Need scenario analysis for which fields are populated
                            scenario = [0,3,5,6,7,10]
                            length = 12
                            #Adjust the positions if there is no wind recorded
                            if len(dets[2].text) > 4:
                                scenario = [0,2,4,5,6,9]
                                length = length-1
                            #Adjust the positions if the performance was not a seasons best or personal best
                            if dets[scenario[1]+1] not in ('SB','PB'): 
                                scenario[2] = scenario[2]-1 
                                scenario[3] = scenario[3]-1
                                scenario[4] = scenario[4]-1
                                scenario[5] = scenario[5]-1
                                length = length -1
                            #Adjust the positions for inclusion of coach and whether it is 
                            #an NEYDL match.
                            if len(dets) != length and 'Youth' not in competitions.meeting :
                                scenario[5] = scenario[5]-1

                            #Variables for the Heat and Position to calculate points
                            r = str(vals[2] if len(vals)>2 else 1),
                            p = str(dets[0].text)[0],

                            #finding the first clube in the list 
                            #by searching fro / and only including up to that text
                            singleclub = dets[scenario[5]].text.find('/')
                            if singleclub != -1:
                                singleclub = dets[scenario[5]].text[0:singleclub:1]
                            else: singleclub = dets[scenario[5]].text
                            #Problems processing athlete id in a small number of cases, 
                            #Escaping the problem in the odd cases of failure
                            try:
                                namecheck = str(dets[scenario[1]]).split('"')[1].split('=')[1] if len(str(dets[scenario[1]]).split('"')) > 1 else ''
                            except: ''
                            r = results(
                                meeting_id = j,
                                event = vals[0],
                                event_age_group = vals[1],
                                race = vals[2] if len(vals)>2 else 1,
                                pos = dets[0].text,
                                perf = dets[1].text,
                                name = dets[scenario[1]].text,
                                age_group = dets[scenario[3]].text,
                                gender = dets[scenario[4]].text,
                                club = singleclub,
                                athlete_id = namecheck,
                                points = league_points_calc(r[0],p[0]),
                                event_group = geteventgroup(vals[0])
                            )
                            r.save()
            except:''
    end = default_timer()
    return HttpResponse('Meet Loaded ' + repr(end-start))
