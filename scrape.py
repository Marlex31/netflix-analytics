
from requests_html import HTMLSession

session = HTMLSession()
resp = session.get("https://unogs.com/search/2001: A space odyssey")
resp.html.render(sleep=2)


matches = resp.html.find('span')
counter=0

for match in matches:
	
	if counter == 5: break

	if 'html:title' in match.attrs.values():
		print(match.text)

	elif 'html:vtype' in match.attrs.values():
		print(match.text)

	elif 'html:runtime' in match.attrs.values():
		print(match.text)
		counter+=1
		print()
