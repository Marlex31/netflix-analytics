
from requests_html import HTMLSession
from googlesearch import search

media = "Code Geass: Lelouch of the Rebellion"

session = HTMLSession()
resp = session.get(f"https://unogs.com/search/{media}")
try:
	resp.html.render(sleep=2)
except: # rarely this is triggered, unknown cause
	print("Exception hit")
	resp.html.render(sleep=2)	

matches = resp.html.find('span')
counter=0

for match in matches:
	
	if counter == 4: break

	if 'html:title' in match.attrs.values():
		dummy_title = match.text # for searching the other results on imdb
		print(match.text)

	elif 'html:vtype' in match.attrs.values():
		print(match.text)

	elif 'html:runtime' in match.attrs.values():
		
		if match.text == '--':
			query = f"imdb {dummy_title}"
			for link in search(query, tld="com", num=1, stop=1): pass # this can't be right
			
			session = HTMLSession()
			r = session.get(link)

			duration = r.html.find("time", first=True)
			print(duration.text)

		else: print(match.text)

		counter+=1
		print()
