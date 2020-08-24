import csv
import datetime
import re

def csv_reader(file, index=0):
    with open(file, 'r', encoding="utf8") as f:
        f_read = csv.reader(f)
        next(f_read)

        for line in f_read:
            yield line[index]


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


def convert_time(time_input):

    if re.search(r'[a-zA-Z]', str(time_input)) is None:
        return str(datetime.timedelta(seconds=int(time_input))).split(':00')[0]

    time_input = time_input.replace('min', 'm').strip().replace(' ', '')
    if time_input == "--":  # or '' prob not working
        return None
    elif time_input.endswith('s'):
        time_input = time_input[:time_input.find('m')+1]
    if len(time_input) >= 4 <= 5:  # change
        pattern = "%Hh%Mm"
    elif time_input.endswith('m'):
        pattern = "%Mm"
    else:
        pattern = "%Hh"

    if time_input == '':
        return None

    formatted = datetime.datetime.strptime(time_input, pattern).time()
    return datetime.timedelta(hours=formatted.hour, minutes=formatted.minute).seconds


# show_1 = convert_time("10440")
# print(show_1)
# print(type(show_1))
# show_2 = convert_time("58min")

# print(show_1 + show_2)
