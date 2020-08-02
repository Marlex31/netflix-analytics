import csv


def reader(file, index=0):
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
    copy_list = target_list.copy()
    for i in parser(source_dict):
        for k in copy_list:
            if i in k:
                target_list.remove(k)
                source_dict[i]+=1
