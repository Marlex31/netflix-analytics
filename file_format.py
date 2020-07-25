
import csv
import re
from collections import Counter


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

for i in list_1:
	print(i)


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


# glossary = {}

# for title in iter(list_1):
# 	smpl_title = title.split(':')[0]
# 	x=0
# 	for i in list_1:
# 		if smpl_title in i:
# 			x+=1
# 	glossary.update({smpl_title:x})

# print(glossary)