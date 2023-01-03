import json
import csv
import datetime
from collections import Counter, OrderedDict
from itertools import chain
import calendar

from matplotlib import pyplot as plt
import numpy as np


with open("db.json", "r", encoding="utf-8") as f:
    json_db = json.loads(f.read())

with open("netflix.csv", "r", encoding="utf8") as f:
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
dates = []
for i in titles_counter.items():
    for j, k in i[1].items():
        date = j.split("/")
        year = "20" + date[-1]
        if year not in activity.keys():
            days = 365
            if calendar.isleap(int(year)):
                days += 1

            activity.update({year: np.zeros(days).tolist()})

        date = list(map(int, date))
        date.reverse()
        dummy_date = date.copy()  # necessary?
        date = dummy_date[0], dummy_date[2], dummy_date[1]
        week_day = datetime.date(*date).day
        month = datetime.date(*date).month
        dayof_year = abs(
            (
                datetime.date(int(year), int(month), int(week_day))
                - datetime.date(int(year), 1, 1)
            ).days
            + 1
        )  # why addition

        dates.append(
            (dayof_year, (datetime.date(int(year), int(month), int(week_day))))
        )
        activity[year][dayof_year] = round(json_db[i[0]][2] * k, 2)

activity = dict(OrderedDict(sorted(activity.items())))
# print(activity)
y = list(chain.from_iterable(activity.values()))

slice_len = int(round(len(json_db), ndigits=-1) / 10)
max_vals = sorted(y, reverse=True)[:slice_len]
thresh = round(np.mean(max_vals)) - round(np.std(y), 2)

years = list((activity.keys()))
search = []
indicies = []
for i in max_vals:
    if i > thresh:
        index = y.index(i)
        start = 0
        end = 365
        for year in years:
            days = 365
            if calendar.isleap(int(year)):
                days += 1
            if start <= index <= end:
                indicies.append(index)
                search.append((index - start, int(year)))
                break
            start += days
            end += days

indicies = sorted(indicies)
labels = []
for i in search:
    for j in dates:
        if i[0] == j[0] and i[1] == j[1].year:
            label = j[1].month, j[1].day, j[1].year
            label = list(map(str, label))
            label[2] = label[2].replace("20", "", 1)
            label = "/".join(label)
            labels.append(label)
            break

# print(search)
# print(labels)

annotations = []
for label in labels:
    names = []
    nums = []
    for key, val in titles_counter.items():
        for v in val.items():
            if label == v[0]:
                names.append(key)
                nums.append(v[1])
    annotations.append(names[nums.index(max(nums))])
annotations = [x.split(":")[0] for x in annotations]
# print(annotations)

# def max_vals(a, n):
#     M = a.shape[0]
#     perc = (np.arange(M-n, M)+1.0)/M*100
#     return np.percentile(a, perc, interpolation='nearest')

# print(max_vals(np.array(y), 10))

# print(annotations)
# print(max_vals)
# print(indicies)

# day_thresh = 200
# last = 0
# index = 0
# for i in indicies:
#     #  and max_vals[index] - max_vals[index-1] > 1
#     if i - last <= day_thresh and i >= day_thresh:
#         index = indicies.index(i)
#         annotations.pop(index)
#         max_vals.pop(index)
#         indicies.pop(index)
#     last = i

fig, ax = plt.subplots(figsize=(10, 5))
X = list(range(len(y)))
(line,) = ax.plot(X, y)

# annotations.pop(0)
# max_vals.pop(1)
# indicies.pop(1)

ordered_vals = []
for i in y:
    if i in max_vals:
        ordered_vals.append(i)

# print()
# print(annotations)
# print(ordered_vals)
# print(indicies)
# print(labels)
# print(search)

indicies = iter(indicies)
ordered_vals = iter(ordered_vals)
for title in annotations:
    ax.annotate(
        title,
        xy=(next(indicies), next(ordered_vals)),
        xycoords="data",
        xytext=(5, 0),
        textcoords="offset points",
        # arrowprops=dict(facecolor="black", shrink=0.05),
        horizontalalignment="right",
        verticalalignment="bottom",
    )

plt.title("Total watch time")
plt.xlabel("Days")
plt.ylabel("Hours watched")
plt.show()
