import sqlite3
import pandas as pd
from dataload.models import athlete, performances


def performancecounts():
    db = sqlite3.connect('db.sqlite3')
    rankingquery = db.cursor()
    sql = 'select event, date, count(*) as Performances '
    sql += 'from dataload_performances p INNER JOIN dataload_athlete a on '
    sql += 'a.athlete_id = p.athlete_id ' 
    sql += 'where club_at_performance LIKE "%Durham%"'
    sql += ' Group by event, date'
    rankingquery.execute(sql) 
    r = pd.DataFrame(rankingquery.fetchall(), columns = [x[0] for x in rankingquery.description])
    
    return r
