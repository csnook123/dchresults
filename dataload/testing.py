from datetime import datetime

d = 'Sat 18 Jun 2023'
e = "%d %b %Y"
d = d[4:len(d):1]
dateformatting = datetime.strptime(d,e)
print(dateformatting)