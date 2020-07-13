import imdb

ia = imdb.IMDb()
media = 'Jimmy Carr: Funny Business'

# search = ia.search_movie(media)
# print(search[0].movieID)

search = ia.search_episode(f'{media} Funny Business') # search_episode and search_movie 
for i in search:
	print(i.data['kind']) # use data['kind'], data['episode of']

# print(dir(i))
