
from requests_html import HTMLSession
from googlesearch import search

class mediaSearch(object):
	"""docstring for mediaSearch"""
	def __init__(self, media, len_scrape=False):
		super(mediaSearch, self).__init__()

		self.media = media
		self.len_scrape = len_scrape

		self.title = media
		self.media_type = None 
		self.duration = None

		self.simple_media = media.split(':')[0] # had a space after colon
		self.session = HTMLSession()
		self.session.browser


		if self.len_scrape == True:
			self.imdb_search()
		else:
			self.unogs_search()

	def unogs_search(self):

		 r = self.session.get(f"https://unogs.com/search/{self.media}")
		 r.html.render(sleep=2, timeout=14.0)

		 matches = r.html.find('span')
		 counter=0
		 first_match = None


		 for match in matches:
		 	
		 	if counter == 5: # scraping limit
		 		if first_match in self.media:
		 			self.title = first_match # failsafe for not finding an exact result (eg Chapter 2 and Chapter two)
		 			self.imdb_search()

		 		elif self.title not in self.media:
		 			self.title = None
		 			self.media_type = None
		 			break # remove from list

		 		break


		 	if 'html:title' in match.attrs.values():
		 		self.title = match.text

		 		if counter == 0:
		 			first_match = self.title

		 	elif 'html:vtype' in match.attrs.values():
		 		self.media_type = match.text

		 	elif 'html:runtime' in match.attrs.values():
		 		self.duration = match.text

		 		if self.title == self.simple_media or self.title == self.media: # or self.title in self.media

		 			# searching the lenght on imdb
		 			self.imdb_search()
		 			break

		 		counter+=1


	def imdb_search(self):

		for link in search(f"imdb {self.title}", tld="com", num=1, stop=1): pass

		r = self.session.get(link)
		try:
			self.duration = r.html.find("time", first=True).text
		except AttributeError:
			for link in search(f"imdb {self.simple_media}", tld="com", num=1, stop=1): pass
			r = self.session.get(link)
			self.duration = r.html.find("time", first=True).text


# ex = mediaSearch('The Hangover: Part III')
# print()
# print(ex.media)
# print(ex.title)
# print(ex.media_type)
# print(ex.duration)