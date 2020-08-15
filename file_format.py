
import re
import concurrent.futures
from itertools import repeat
import os.path
import json

from scrape import mediaSearch
from utillities import csv_reader, ep_group, parser


file = 'netflix.csv'

titles = []
movies = []
for line in csv_reader(file):
    if line.find(':') != -1:  # -1 is the ret value for no search yield
        titles.append(line)
    else:
        movies.append(line)

colon_pattern = re.compile(r":")
set_1 = set()
set_2 = set()
set_3 = set()

for title in titles:
    x = 0
    matches = colon_pattern.finditer(title)
    for match in matches:
        x += 1

        if x == 1:
            set_1.add(title)

        elif x == 2:
            set_2.add(title)

        elif x == 3:
            set_3.add(title)

list_1 = list(set_1.difference(set_2))
list_1.sort()

list_2 = list(set_2.difference(set_3))
list_2.sort()

list_3 = list(set_3)
list_3.sort()


# list_1 handling
glossary_1 = {}
glossary_2 = {}

for title in list_1:
    smpl_title = title.split(':')[0]

    x = 0
    for i in list_1:
        if smpl_title+':' in i:
            x += 1

    if x < 7:
        if x > 1:
            if smpl_title in glossary_2.keys():
                glossary_2[smpl_title].append(title.split(':')[1])
            else:
                glossary_2.update({smpl_title: [x, title.split(':')[1]]})

        else:
            glossary_2.update({title: [x, '']})

    else:
        glossary_1.update({smpl_title: x})


ep_group(glossary_1, list_2)


global glossary_3
glossary_3 = {}
global to_search
to_search = []

if __name__ == '__main__':

    if os.path.exists("db.json") is True:
        print('DB found, stopping program execution...')
        exit()

    else:
        with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:
            results = executor.map(mediaSearch, parser(glossary_2))

            for r in results:
                if r.media_type != 'series':
                    glossary_3.update({r.title: [r.media_type, r.genres, r.duration]})
                else:
                    occurences = glossary_2[r.title][0]  # possible need for exceptions
                    glossary_3.update({r.title: [r.media_type, r.genres, r.duration, occurences]})

            try:
                glossary_3.pop(None)
            except KeyError:
                pass

            for i, j in glossary_3.items():
                if None in j:  # is the occurences var required?
                    ex = mediaSearch(i)
                    glossary_3[i] = [ex.media_type, ex.genres, ex.duration]

            for i, j in glossary_2.items():
                if j[0] > 1:
                    for k in glossary_3.keys():
                        if k.startswith(i):
                            for item in j[2:]:
                                if glossary_3[k][0] == 'movie' and f'{i}:{item}' not in glossary_3.keys():
                                    to_search.append(f'{i}:{item}')

# list_2 handling
glossary_4 = {}
for title in list_2:
    smpl_title = title.split(':')[0]
    if smpl_title in glossary_4.keys():
        glossary_4[smpl_title] += 1
    else:
        glossary_4.update({smpl_title: 1})

copy_dict = glossary_4.copy()
for i, j in copy_dict.items():
    if j < 3:
        glossary_4.pop(i)

ep_group(glossary_4, list_3)


# list_3 handling
season_pattern = re.compile(r': ((Season|Part) \d):')
found = []
names = []

for title in list_3:
    matches = season_pattern.finditer(title)
    for match in matches:

        if match.group(2) == 'Season' or match.group(2) == 'Part':
            name = title[0:match.span()[0]]
            # season = match.group(1)
            # episode = title[match.span()[-1]:].strip()

            found.append(title)
            names.append(name)
            # print(name, season, episode, sep=' - ')

for i in list_3:
    if i not in found:
        to_search.append(i)

glossary_5 = {}
for title in names:
    if title in glossary_5.keys():
        glossary_5[title] += 1
    else:
        glossary_5.update({title: 1})

copy_dict = glossary_5.copy()
for i, j in copy_dict.items():
    if j < 3:
        glossary_5.pop(i)

if __name__ == '__main__':
    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:
        glossary_6 = {**glossary_1, **glossary_4, **glossary_5}
        results = executor.map(mediaSearch, parser(glossary_6), repeat(True))

        for r in results:
            occurences = glossary_6[r.media]
            glossary_6[r.media] = ['series', r.genres, r.duration, occurences]

# if to_search:
#     with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:

#         results = executor.map(mediaSearch, to_search, repeat(True))
#         for r in results:
#             glossary_3.update({r.title: ['movie', r.genres, r.duration]})
# print(to_search)

        merged_dict = {**glossary_6, **glossary_3}
        with open('db.json', 'w', encoding='utf8') as w:
            json.dump(merged_dict, w, indent=4)
