import datetime


date = datetime.date.today()

record = '2023-05-24'

record = datetime.datetime.strptime(record, '%Y-%m-%d').date()
print(date)
print(record)

print((record - date).days)
