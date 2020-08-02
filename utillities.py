import csv
import datetime
import json

from collections import Counter


def csv_reader(file, index=0):
    with open(file, 'r', encoding="utf8") as f:
        f_read = csv.reader(f)
        next(f_read)

        for line in f_read:
            yield line[index]


def json_reader():
    with open('db.json', 'r', encoding='utf8') as f:
        return json.load(f)


def json_writer(data):
    with open('db.json', 'w', encoding='utf8') as w:
        json.dump(data, w, indent=4)


def parser(data):
    for i, j in data.items():
        if type(j) is list and j[1] == '' or type(j) is int:
            yield i
        else:
            yield f'{i}:{j[1]}'


def ep_group(source_dict, target_list):
    # add ret statement
    copy_list = target_list.copy()
    for i in parser(source_dict):
        for k in copy_list:
            if i in k:
                target_list.remove(k)
                source_dict[i] += 1


def ep_counter(data, formatted=True):
    output = Counter(data)
    copy_dict = dict(output.copy())

    for x, y in copy_dict.items():
        if y < 3:
            output.pop(x)

    return output


def watchTime(time_input):
    if len(time_input) == 5:
        pattern = "%Mmin"
    else:
        pattern = "%Hh %Mmin"
    formatted = datetime.datetime.strptime(time_input, pattern).time()
    return datetime.timedelta(hours=formatted.hour, minutes=formatted.minute)


# show_1 = watchTime("2h 30min")
# show_2 = watchTime("58min")

# print(show_1 + show_2)
