
import csv
import re
from collections import Counter
import concurrent.futures

from scrape import mediaSearch
from itertools import repeat

file = 'netflix.csv'

def reader(file, index=0): 
 
	with open(file, 'r', encoding="utf8") as f:
		f_read = csv.reader(f)
		next(f_read)

		for line in f_read:
			yield line[index]

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

for title in iter(list_1):
	smpl_title = title.split(':')[0]

	x=0
	for i in list_1:
		if smpl_title+':' in i:
			x+=1

	# add break rule for already existing titles
	if x < 7:
		if x > 1:
			glossary_2.update({smpl_title:[x, title.split(':')[1]]})
		else:
			glossary_2.update({title:[x, '']})
	
	else:
		glossary_1.update({smpl_title:x})


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


ep_group(glossary_1, list_2)
# print(glossary_1)
# print()
# print(glossary_2)


def main():
	if __name__ == '__main__':


		with concurrent.futures.ProcessPoolExecutor(max_workers=3) as executor: # thread pool exec if just imdb reqs
			results = executor.map(mediaSearch, parser(glossary_2))

			for result in results:
				
				print(result.media)
				print(result.title)
				print(result.media_type)
				print(result.duration)
				print()

# main()