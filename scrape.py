
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

        if self.len_scrape is True:
            self.duration = self.imdb_search()
        else:
            self.unogs_search()

    def unogs_search(self):

        r = self.session.get(f"https://unogs.com/search/{self.media}")
        r.html.render(sleep=2, timeout=20.0)
        matches = r.html.find('span')
        counter = 0
        first_title = None
        first_media_type = None

        for match in matches:
            if counter == 5:  # scraping limit
                if first_title in self.media:
                    self.title = first_title  # failsafe for not finding an exact result
                    self.media_type = first_media_type
                    self.duration = self.imdb_search()

                elif self.title not in self.media:
                    self.title = None
                    self.media_type = None
                    self.duration = None
                    break
                break

            if 'html:title' in match.attrs.values():
                self.title = match.text
            elif 'html:vtype' in match.attrs.values():
                self.media_type = match.text
            elif 'html:runtime' in match.attrs.values():
                self.duration = match.text
                if counter == 0:
                    first_title = self.title
                    first_media_type = self.media_type
                    first_duration = self.duration
                if (self.title == self.media or
                        self.title == self.simple_media):  # or self.title in self.media
                    self.duration = self.imdb_search()
                    if (self.media_type == 'movie' and
                            len(self.media.split(':')) != len(self.title.split(':'))):
                        self.title = first_title
                        self.media_type = first_media_type
                        self.duration = first_duration
                    break
                counter+=1

    def imdb_search(self):

        for link in search(f"imdb {self.title}", tld="com", num=1, stop=1): pass
        r = self.session.get(link)
        try:
            return r.html.find("time", first=True).text
        except AttributeError:
            for link in search(f"imdb {self.simple_media}", tld="com", num=1, stop=1): pass
            r = self.session.get(link)
            return r.html.find("time", first=True).text


# ex = mediaSearch('The Hangover: Part III')
# print(ex.media)
# print(ex.title)
# print(ex.media_type)
# print(ex.duration)
