from datetime import datetime
from datetime import date

strdate="2020-10-16 12:35:20" 
dt_tuple=tuple([int(x) for x in strdate[:10].split('-')])+tuple([int(x) for x in strdate[11:].split(':')])
# print(dt_tuple)

today = datetime.today()
datetimeobject = datetime.strptime("14/10/2021 21:00", "%d/%m/%Y %H:%M")
print(today > datetimeobject)