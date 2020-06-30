import imdb

ia = imdb.IMDb()
show = 'DEATH NOTE'

# search = ia.search_movie('Death note')
# print(search[0].movieID)

search = ia.search_episode(f'{show} Pursuit') # search_episode and search_movie 
for i in search:
	print(i.data['kind']) # use data['kind'], data['episode of']

# print(dir(i))
