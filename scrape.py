
from requests_html import HTMLSession
from googlesearch import search

from utillities import convert_time


class mediaSearch(object):

    def __init__(self, media, len_scrape=False, placeholder_len='25min'):
        super(mediaSearch, self).__init__()

        self.media = media
        self.len_scrape = len_scrape
        self.placeholder_len = placeholder_len

        self.title = media
        self.media_type = None
        self.duration = None
        self.genres = []

        self.simple_media = media.split(':')[0]  # had a space after colon
        self.session = HTMLSession()

        if self.len_scrape is True:
            self.duration = convert_time(self.imdb_search())
        else:
            self.unogs_search()
            self.imdb_search()

    def unogs_search(self):

        r = self.session.get(f"https://unogs.com/search/{self.media}")
        r.html.render(sleep=2, timeout=20.0)
        matches = r.html.find('span')
        self.counter = 0
        first_title = None
        first_media_type = None

        for match in matches:
            if self.counter == 5:  # scraping limit
                if first_title in self.media:
                    self.title = first_title  # failsafe for not finding an exact result
                    self.media_type = first_media_type
                    self.duration = convert_time(self.imdb_search())

                elif self.title not in self.media:
                    self.title = None
                    self.media_type = None
                    self.duration = None

                break

            if 'html:title' in match.attrs.values():
                self.title = match.text
            elif 'html:vtype' in match.attrs.values():
                self.media_type = match.text

            elif 'html:runtime' in match.attrs.values():
                print(match.text)
                self.duration = convert_time(match.text)
                if self.counter == 0:
                    first_title = self.title
                    first_media_type = self.media_type
                    first_duration = self.duration
                if (self.title == self.media or self.title == self.simple_media):  # or self.title in self.media
                    if (self.media_type == 'movie' and
                            len(self.media.split(':')) != len(self.title.split(':'))):
                        self.title = first_title
                        self.media_type = first_media_type
                        self.duration = first_duration
                    elif self.media_type == 'series':
                        self.duration = convert_time(self.imdb_search())
                    break
                self.counter += 1

    def imdb_search(self):

        if self.len_scrape is True or self.media_type == 'series' or self.counter == 5 and self.media_type is not None:

            try:
                link = next(search(f"imdb {self.title}", tld="com", num=1, stop=1))
                r = self.session.get(link)
                genre_list = r.html.find('.inline', containing='Genres')[1].text.split('\n')[1].split('|')
                self.genres = list(map(str.strip, genre_list))
                return r.html.find("time", first=True).text

            except AttributeError:
                link = next(search(f"imdb {self.simple_media}", tld="com", num=1, stop=1))
                r = self.session.get(link)
                genre_list = r.html.find('.inline', containing='Genres')[1].text.split('\n')[1].split('|')
                self.genres = list(map(str.strip, genre_list))
                duration = r.html.find("time", first=True)  # in case of no info
                if duration is None:
                    return self.placeholder_len
                return duration.text

        elif self.media_type is not None:  # necessary?
            link = next(search(f"imdb {self.title}", tld="com", num=1, stop=1))
            r = self.session.get(link)
            genre_list = r.html.find('.inline', containing='Genres')[1].text.split('\n')[1].split('|')
            self.genres = list(map(str.strip, genre_list))


ex = mediaSearch('Happy Tree Friends: Four on the Floor')
print(ex.media)
print(ex.title)
print(ex.media_type)
print(ex.duration)
print(ex.genres)
