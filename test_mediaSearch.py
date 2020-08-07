
from scrape import mediaSearch

# duration is compared as a string since it is a datetime.timedelta obj


def test_1():
    # unogs has ElCamino movie as first result
    result = mediaSearch('Breaking Bad')

    assert result.title == 'Breaking Bad'
    assert result.media_type == 'series'
    assert str(result.duration) == '0:49:00'
    assert result.genres == ['Crime', 'Drama', 'Thriller']


def test_2():

    result = mediaSearch('2001: A Space Odyssey')

    assert result.title == '2001: A Space Odyssey'
    assert result.media_type == 'movie'
    assert str(result.duration) == '2:28:00'
    assert result.genres == ['Adventure', 'Sci-Fi']


def test_3():
    # netflix csv vs unogs db name
    result = mediaSearch('His Dark Materials: The Golden Compass')

    assert result.title == 'The Golden Compass'
    assert result.media_type == 'movie'
    assert str(result.duration) == '1:48:00'
    assert result.genres == ['Adventure', 'Family', 'Fantasy']


def test_4():

    result = mediaSearch('Kakegurui: Episode 4')

    assert result.title == 'Kakegurui'
    assert result.media_type == 'series'
    assert str(result.duration) == '0:24:00'
    assert result.genres == ['Animation', 'Drama', 'Mystery', 'Thriller']


def test_5():
    # removed from both DBs
    result = mediaSearch('Happy Tree Friends: The Third Degree')

    assert result.title is None
    assert result.media_type is None
    assert result.duration is None
    assert bool(result.genres) is False  # better way?
