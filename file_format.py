
import csv
import re

# formats the netflix csv file by removing extra colons from media name or episode title, criteria is more than 3 colons
# also removes shows that have only one episode watched


file = 'netflix.csv'

def reader(file, index=0): 
 
	with open(file, 'r', encoding="utf8") as f:
		f_read = csv.reader(f)
		next(f_read)

		for line in f_read:
			yield line[index]


titles = []
for line in reader(file):
	titles.append(line)

colon_pattern = re.compile(r":")
# title_pattern = re.compile(r"^(([a-zA-Z0-9_'\/,]+\s?)*):")
# x=0
# for title in titles:
# 	matches = title_pattern.finditer(title)
# 	for match in matches:
# 		print(x, match.group(1))
# 		x+=1


for title in titles:
	x=0
	matches = colon_pattern.finditer(title)
	for match in matches:
		x+=1
		if x == 3:
			# print(title)
			# print(match)
			print(title[0:match.span()[0]])



# titles = ["Code Geass: Lelouch of the Rebellion: Season 2: Episode 25", "Fate/stay night: Unlimited Blade Works: Part 2: Epilogue",
# "JoJo's Bizarre Adventure: Stardust Crusaders: Dio's World, Part 3", "Fate/Apocrypha: Part 1: Apocrypha: The Great Holy Grail War"]

# season_pattern = re.compile(r': ((Season|Part) \d):')

# for title in titles:
# 	matches = season_pattern.finditer(title)

# 	for match in matches:

# 		if match.group(2) == 'Season' or match.group(2) == 'Part':
# 			season = match.group(1)
# 			name = title[0:match.span()[0]]
# 			episode = title[match.span()[-1]:].strip()

# 			print(name, season, episode, sep=' - ')
