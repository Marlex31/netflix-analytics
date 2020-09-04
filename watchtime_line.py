
import json
import csv
import datetime
from collections import Counter
from matplotlib import pyplot as plt
from itertools import chain
import calendar
import numpy as np
import datetime
from pprint import pprint


with open('db.json', 'r', encoding='utf-8') as f:
    json_db = json.loads(f.read())

with open('netflix.csv', 'r', encoding="utf8") as f:
    f_read = csv.reader(f)
    next(f_read)
    csv_db = [line for line in f_read]

titles_counter = {}
for item in json_db.keys():
    for title in csv_db:
        if title[0].startswith(item):
            if item not in titles_counter.keys():
                titles_counter.update({item: []})
            titles_counter[item].append(title[1])

for i, j in titles_counter.items():
    titles_counter[i] = dict(Counter(j))


activity = {}
for i in titles_counter.items():
    for j, k in i[1].items():
        date = j.split('/')
        year = '20' + date[-1]
        if year not in activity.keys():
            if not calendar.isleap(int(year)):
                days = 365
            else:
                days = 366

            activity.update({year: np.zeros(days).tolist()})

        date = list(map(int, date))
        date.reverse()
        dummy_date = date.copy()
        date = dummy_date[0], dummy_date[2], dummy_date[1]
        week_day = datetime.date(*date).weekday() + 1
        month = datetime.date(*date).month

        date = abs((datetime.datetime(int(year), int(month), int(week_day)) -
                    datetime.datetime(int(year), 1, 1)).days + 1)
        # print(date)
        # if k > 10:
        #     print(month, week_day, year, k)

        activity[year][date] = round(json_db[i[0]][2] * k, 2)

# print(activity)


y = list(chain.from_iterable(activity.values()))
X = list(range(len(y)))

plt.plot(X, y)
plt.title('Watch time in ALL YEARS')
plt.show()
