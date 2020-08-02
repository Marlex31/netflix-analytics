
from scrape import mediaSearch


def test_1():
    # unogs has ElCamino movie as first result
    result = mediaSearch('Breaking Bad')

    assert result.title == 'Breaking Bad'
    assert result.media_type == 'series'
    assert result.duration == '49min'


def test_2():

    result = mediaSearch('2001: A Space Odyssey')

    assert result.title == '2001: A Space Odyssey'
    assert result.media_type == 'movie'
    assert result.duration == '2h 29min'


def test_3():
    # netflix csv vs unogs db name
    result = mediaSearch('His Dark Materials: The Golden Compass')

    assert result.title == 'The Golden Compass'
    assert result.media_type == 'movie'
    assert result.duration == '1h 53min'


def test_4():

    result = mediaSearch('Kakegurui: Episode 4')

    assert result.title == 'Kakegurui'
    assert result.media_type == 'series'
    assert result.duration == '24min'


def test_5():
    # removed from both DBs
    result = mediaSearch('Happy Tree Friends: The Third Degree')

    assert result.title is None
    assert result.media_type is None
    assert result.duration is None
