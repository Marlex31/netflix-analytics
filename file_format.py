
import re
import concurrent.futures
from itertools import repeat
from pprint import pprint

from scrape import mediaSearch
from utillities import *


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


if __name__ == '__main__':
    try:
        glossary_3 = json_reader()

    except FileNotFoundError:
        glossary_3 = {}
        with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:
            results = executor.map(mediaSearch, parser(glossary_2))

            for r in results:

                if r.media_type != 'series':
                    glossary_3.update({r.title: [r.media_type, r.duration]})
                else:
                    occurences = glossary_2[r.title][0]  # possible need for exceptions
                    glossary_3.update({r.title: [r.media_type, r.duration, occurences]})

            try:
                glossary_3.pop(None)
            except KeyError:
                pass

            for i, j in glossary_3.items():
                if None in j:
                    ex = mediaSearch(i)
                    glossary_3[i] = [ex.media_type, ex.duration]


to_search = []
for i, j in glossary_2.items():
    if j[0] > 1:
        for k in glossary_3.keys():
            if k.startswith(i):
                for item in j[2:]:
                    if glossary_3[k][0] == 'movie' and f'{i}:{item}' not in glossary_3.keys():
                        to_search.append(f'{i}:{item}')

if to_search:
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        results = executor.map(mediaSearch, parser(glossary_1), repeat(True))

        for r in results:
            occurences = glossary_1[r.media]
            glossary_1[r.media] = ['series', r.duration, occurences]
        glossary_3.update(glossary_1)

        results = executor.map(mediaSearch, to_search, repeat(True))
        for r in results:
            glossary_3.update({r.title: ['movie', r.duration]})

        json_writer(glossary_3)

# print(glossary_3)


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


# glossary_5 = {}
# with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
#         results = executor.map(mediaSearch, parser(glossary_4), repeat(True))

#         for r in results:
#             occurences = glossary_4[r.media]
#             glossary_4[r.media] = ['series', r.duration, occurences]
#         glossary_5.update(glossary_4)
# print(glossary_5)


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

# print(ep_counter(names))

not_found = []
for i in list_3:
    if i not in found:
        not_found.append(i)
# print(not_found)
