
from requests_html import HTMLSession
from googlesearch import search

class mediaSearch(object):
	"""docstring for mediaSearch"""
	def __init__(self, media):
		super(mediaSearch, self).__init__()

		self.media = media
		self.simple_media = media.split(': ')[0]
		self.session = HTMLSession()

		self.unogs_search()

	def unogs_search(self):

		 resp = self.session.get(f"https://unogs.com/search/{self.media}")
		 resp.html.render(sleep=2, timeout=12.0)

		 matches = resp.html.find('span')
		 counter=0
		 first_match = None


		 for match in matches:
		 	
		 	if counter == 5: # scraping limit
		 		if first_match in self.media:
		 			self.title = first_match # failsafe for not finding an exact result (eg Chapter 2 and Chapter two)
		 			self.duration = self.imdb_search()
		 		
		 		else: # for shows that have been removed from the database
		 			self.title = None
		 			self.media_type = None 
		 			self.duration = None

		 		break


		 	if 'html:title' in match.attrs.values():
		 		self.title = match.text

		 		if counter == 0:
		 			first_match = self.title

		 	elif 'html:vtype' in match.attrs.values():
		 		self.media_type = match.text

		 	elif 'html:runtime' in match.attrs.values():
		 		self.duration = match.text

		 		if self.title == self.simple_media or self.title in self.media:

		 			# searching the lenght on imdb
		 			self.duration = self.imdb_search()
		 			break

		 		elif self.title not in self.media:
		 			pass # remove from list

		 		counter+=1


	def imdb_search(self):

		for link in search(f"imdb {self.title}", tld="com", num=1, stop=1): pass

		r = self.session.get(link)
		ep_lenght = r.html.find("time", first=True).text

		return ep_lenght


	def result(self):

		return [self.title, self.media_type, self.duration]