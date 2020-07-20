
from requests_html import HTMLSession
from googlesearch import search

media = "John Wick: Chapter 2"

session = HTMLSession()
resp = session.get(f"https://unogs.com/search/{media}")
try:
	resp.html.render(sleep=2)
except Exception as e: # request timeout error, exceeds 800ms
	print(e)
	resp.html.render(sleep=2)	


matches = resp.html.find('span')
counter=0
first_match = None # failsafe for not finding an exact result (eg Chapter 2 and Chapter two)

for match in matches:
	
	if counter == 4: # scraping limit
		title = first_match
		break

	if 'html:title' in match.attrs.values():
		title = match.text

		if counter == 0:
			first_match = title

	elif 'html:vtype' in match.attrs.values():
		media_type = match.text

	elif 'html:runtime' in match.attrs.values():
		duration = match.text

		if title == media:
			
			# searching the lenght on imdb
			if media_type == 'series':
				for link in search(f"imdb {title}", tld="com", num=1, stop=1): pass

				session = HTMLSession()
				r = session.get(link)
				duration = r.html.find("time", first=True).text

			break

		counter+=1


print(title, media_type, duration, sep=', ')