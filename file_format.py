
import csv
import re
from collections import Counter
import concurrent.futures
from itertools import repeat

from scrape import mediaSearch
from utillities import *

file = 'netflix.csv'

titles = []
movies = []
for line in reader(file):
	if line.find(':') > 0:
		titles.append(line)
	else:
		movies.append(line)
		
colon_pattern = re.compile(r":")
# episode_pattern = r":\s?([a-zA-Z0-9_'\/,]+\s?)* [a-zA-Z0-9_'\/,]+$"

set_1 = set()
set_2 = set()
set_3 = set()

for title in titles:
	x=0
	matches = colon_pattern.finditer(title)
	for match in matches:
		x+=1
		
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

# for i in list_1:
# 	print(i)


season_pattern = re.compile(r': ((Season|Part) \d):')
found = []
names = []

for title in list_3:
	matches = season_pattern.finditer(title)

	for match in matches:

		if match.group(2) == 'Season' or match.group(2) == 'Part':
			season = match.group(1)
			name = title[0:match.span()[0]]
			episode = title[match.span()[-1]:].strip()

			found.append(title)
			names.append(name)
# 			print(name, season, episode, sep=' - ')


# not_found = []
# for x in list_3:
# 	if x not in found:
# 		print(x)


# ep_watched = Counter(names)
# copy_dict = ep_watched.copy()

# for x, y in copy_dict.items():
# 	if y < 3:
# 		ep_watched.pop(x)
# 	else:
# 		print(x)

# print(ep_watched)

glossary_1 = {}
glossary_2 = {}

for title in list_1:
	smpl_title = title.split(':')[0]

	x=0
	for i in list_1:
		if smpl_title+':' in i:
			x+=1

	# add break rule for already existing titles
	if x < 7:
		if x > 1:
			if smpl_title in glossary_2.keys():
				glossary_2[smpl_title].append(title.split(':')[1])
			else:
				glossary_2.update({smpl_title:[x, title.split(':')[1]]})
		else:
			glossary_2.update({title:[x, '']})
	
	else:
		glossary_1.update({smpl_title:x})


ep_group(glossary_1, list_2)

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor: # thread pool exec if just imdb reqs
	results = executor.map(mediaSearch, parser(glossary_1), repeat(True))

	for r in results:
		occurences = glossary_1[r.media]
		glossary_1[r.media] = [occurences, r.duration] 

# print(glossary_1)
# print(glossary_2)
# print()

def main():
	glossary_3 = {}

	if __name__ == '__main__':

		with concurrent.futures.ProcessPoolExecutor(max_workers=3) as executor: # thread pool exec if just imdb reqs
			results = executor.map(mediaSearch, parser(glossary_2))

			for r in results:
				if r.media_type != 'series':
					glossary_3.update({r.title:[r.media_type, r.duration]})
				else:
					occurences = glossary_2[r.title][0] # possible need for exceptions
					glossary_3.update({r.title:[r.media_type, r.duration, occurences]})

		print(glossary_3)
# main()


glossary_4 = {'2001: A Space Odyssey': ['movie', '2h 29min'], 'Captain America: The Winter Soldier': ['movie', '2h 16min'], 'EVANGELION: DEATH (TRUE)²': ['movie', '1h 41min'], 'Flavors of Youth: International Version': ['movie', '1h 14min'], None: [None, None], 'The Golden Compass': ['movie', '1h 53min'], 'Jimmy Carr: Funny Business': ['movie', '1h 2min'], 'John Wick': ['movie', '1h 41min'], 'Journey 2: The Mysterious Island': ['movie', '1h 34min'], 'Kakegurui': ['series', '24min', 4], 'Pirates of the Caribbean: Dead Men Tell No Tales': ['movie', '2h 9min'], 'Sword Art Online the Movie: Ordinal Scale': ['movie', '1h 59min'], 'The Hangover: Part III': ['movie', '1h 40min'], 'The Lord of the Rings: The Fellowship of the Ring': ['movie', '2h 58min'], 'The Seven Deadly Sins the Movie: Prisoners of the Sky': ['movie', '1h 39min'], 'Transformers: Dark of the Moon': ['movie', '2h 34min'], 'Underworld: Rise of the Lycans': ['movie', '1h 32min'], 'Violet Evergarden: Eternity and the Auto Memory Doll': ['movie', '1h 30min']}
glossary_4.pop(None)

to_search = []
for i, j in glossary_2.items():
	if j[0] > 1:
		for k in glossary_4.keys():
			if k.startswith(i):
				for item in j[1:-1]:
					if glossary_4[k][0] == 'movie':
						to_search.append(f'{i}:{item}')

# for key in glossary_1.keys():
# 	to_search.append(key)
# print(to_search)