import csv
import re

import imdb


file = 'netflix.csv'

def reader(file, index=0): 
 
	with open(file, 'r', encoding="utf8") as f:
		f_read = csv.reader(f) 
		next(f_read)

		for line in f_read:
			yield line[index]

# titles = []

# for row in reader(file):
# 	titles.append(row)
# 	print(row)

# print(len(titles))


def writer(file, data):
	"""Writes the contents of the lists inside csv files"""

	fieldnames = ['Title', 'Date']
	with open(file, 'w', encoding='utf8', newline='') as w:
		w_write = csv.DictWriter(w, delimiter=',', fieldnames=fieldnames)
		w_write.writeheader()
		for item in data:
			w_write.writerow(item)



media = "Code Geass: Lelouch of the Rebellion: Season 2: Episode 25"

pattern = re.compile(r":")
matches = pattern.finditer(media)

span = []
for match in matches:
	span.append(match.span())


# print(span)
if len(span) == 3: # what if the episode name contains a colon

	name = media[0:span[1][0]]
	season = media[span[1][1]:span[-1][0]].strip()
	episode = media[span[-1][-1]:].strip()


elif len(span) == 2:

	name = media[0:span[0][0]].strip()
	season = media[span[0][1]:span[1][0]].strip()
	episode = media[span[1][1]:].strip()

elif len(span) == 1: # what if it is a movie - compare  by mentions

	name = media[0:span[0][0]].strip()
	episode = media[span[-1][-1]:].strip()
	season = None

else:
	name = media
	episode = None
	season = None

# print(name)
# print(episode)
# print(season)
# print()


# results = []

# ia = imdb.IMDb()
# movie_search = ia.search_movie(media)
# if not movie_search:
# 	 movie_search = ia.search_movie(name)

# # for i in movie_search:
# # 	results.append(i.data['kind'])

# show_search = ia.search_episode(f'{name} {episode}')
# for i in show_search:
# 	results.append(i.data['kind']) # use data['kind'], data['episode of']

# print(results)