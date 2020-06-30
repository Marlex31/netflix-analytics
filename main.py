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
	# print(row)

# print(len(titles))


# case 1

show = "Jimmy Carr: Funny Business"

pattern = re.compile(r":")
matches = pattern.finditer(show)

span = []
for match in matches:
	span.append(match.span())


print(span)
if len(span) == 3: # what if the episode name contains a colon

	name = show[0:span[1][0]]
	season = show[span[1][1]:span[-1][0]].strip()
	episode = show[span[-1][-1]:].strip()


elif len(span) == 2:

	name = show[0:span[0][0]].strip()
	season = show[span[0][1]:span[1][0]].strip()
	episode = show[span[1][1]:].strip()

elif len(span) == 1: # what if it is a movie

	name = show[0:span[0][0]].strip()
	episode = show[span[-1][-1]:].strip()
	season = None

else:
	name = show
	episode = None
	season = None

print(name)
print(episode)
print(season)


