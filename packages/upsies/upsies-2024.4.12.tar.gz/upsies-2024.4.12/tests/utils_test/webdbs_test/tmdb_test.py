from itertools import zip_longest

import pytest

from upsies.utils.types import ReleaseType
from upsies.utils.webdbs import Query, SearchResult, tmdb


@pytest.fixture
def api():
    return tmdb.TmdbApi()


@pytest.mark.parametrize('category', ('movie', 'tv'))
@pytest.mark.parametrize(
    argnames='text, exp_id',
    argvalues=(
        ('Some Title', None),
        ('1984', None),
        ('foo/123', None),
        ('{category}/123', '{category}/123'),
        ('https://www.themoviedb.org/{category}/123', '{category}/123'),
        ('https://www.themoviedb.org/{category}/123-foo-bar-baz', '{category}/123'),
        ('junk {category}/123 more junk', '{category}/123'),
        ('junk https://www.themoviedb.org/{category}/123-foo-bar-baz more junk', '{category}/123'),
    ),
    ids=lambda value: str(value),
)
def test_get_id_from_text(text, category, exp_id, api, store_response):
    text = text.format(category=category)
    if exp_id:
        exp_id = exp_id.format(category=category)
    return_value = api.get_id_from_text(text)
    assert return_value == exp_id


@pytest.mark.asyncio
async def test_search_handles_id_in_query(api, store_response):
    results = await api.search(Query(id='movie/525'))
    assert len(results) == 1

    assert results[0].id == 'movie/525'
    assert results[0].title == 'The Blues Brothers'
    assert results[0].type == ReleaseType.movie
    assert results[0].url == 'http://themoviedb.org/movie/525'
    assert results[0].year == '1980'

    # Make sure we're not awaiting the same coroutine again on subsequent calls
    for _ in range(2):
        assert (await results[0].cast())[:3] == ('Dan Aykroyd', 'John Belushi', 'James Brown')
        assert (await results[0].countries()) == ()
        assert (await results[0].directors()) == ('John Landis',)
        assert (await results[0].genres()) == ('music', 'comedy', 'action', 'crime')
        assert (await results[0].summary()) == (
            'Jake Blues, just released from prison, puts his old band back together '
            'to save the Catholic home where he and his brother Elwood were raised.'
        )
        assert (await results[0].title_english()) == ''
        assert (await results[0].title_original()) == 'The Blues Brothers'


@pytest.mark.asyncio
async def test_search_handles_non_unique_id_in_query(api, store_response):
    results = await api.search(Query(id='525'))
    assert len(results) == 2
    assert results[0].id == 'movie/525'
    assert results[1].id == 'tv/525'


@pytest.mark.asyncio
async def test_search_returns_empty_list_if_title_is_empty(api, store_response):
    assert await api.search(Query('', year='2009')) == []

@pytest.mark.asyncio
async def test_search_returns_list_of_SearchResults(api, store_response):
    results = await api.search(Query('Star Wars'))
    for result in results:
        assert isinstance(result, SearchResult)


@pytest.mark.parametrize(
    argnames=('query', 'exp_result'),
    argvalues=(
        (Query('alien', year='1979', type=ReleaseType.movie), {'title': 'Alien', 'year': '1979'}),
        (Query('alien', year='1986', type=ReleaseType.movie), {'title': 'Aliens', 'year': '1986'}),
        (Query('january', year='2012', type=ReleaseType.movie), {'title': 'One Day in January', 'year': '2012'}),
        (Query('january', year='2015', type=ReleaseType.movie), {'title': 'January Hymn', 'year': '2015'}),
    ),
    ids=lambda value: str(value),
)
@pytest.mark.asyncio
async def test_search_for_year(query, exp_result, api, store_response):
    results = await api.search(query)
    results_title_year = [
        {'title': r.title, 'year': r.year}
        for r in results
    ]
    assert exp_result in results_title_year


@pytest.mark.parametrize(
    argnames=('query', 'exp_titles'),
    argvalues=(
        (Query('Lost & Found Music Studios', type=ReleaseType.series), ('Lost & Found Music Studios',)),
        (Query('Lost & Found Music Studios', type=ReleaseType.movie), ()),
        (Query('Deadwood', type=ReleaseType.movie), ('Deadwood: The Movie',)),
        (Query('Deadwood', type=ReleaseType.series), ('Deadwood',)),
    ),
    ids=lambda value: str(value),
)
@pytest.mark.asyncio
async def test_search_for_type(query, exp_titles, api, store_response):
    results = await api.search(query)
    titles = {r.title for r in results}
    if exp_titles:
        for exp_title in exp_titles:
            assert exp_title in titles
    else:
        assert not titles


@pytest.mark.parametrize(
    argnames=('query', 'exp_cast'),
    argvalues=(
        (Query('The Blues Brothers', year=1980, type=ReleaseType.movie), ('Dan Aykroyd', 'John Belushi')),
        (Query('February', year=2017, type=ReleaseType.movie), ('Ana Sofrenović', 'Aleksandar Đurica', 'Sonja Kolačarić')),
        (Query('Deadwood', year=2004, type=ReleaseType.series), ('Timothy Olyphant', 'Ian McShane')),
    ),
    ids=lambda value: str(value),
)
@pytest.mark.asyncio
async def test_search_result_cast(query, exp_cast, api, store_response):
    results = await api.search(query)
    result = [r for r in results if r.title == query.title][0]
    cast = await result.cast()
    for member in exp_cast:
        assert member in cast


@pytest.mark.asyncio
async def test_search_result_countries(api, store_response):
    results = await api.search(Query('Star Wars'))
    for result in results:
        countries = await result.countries()
        assert countries == ()


@pytest.mark.parametrize(
    argnames=('query', 'exp_id'),
    argvalues=(
        (Query('The Blues Brothers', year=1980, type=ReleaseType.movie), 'movie/525'),
        (Query('February', year=2017, type=ReleaseType.movie), 'movie/700711'),
        (Query('Deadwood', year=2004, type=ReleaseType.series), 'tv/1406'),
    ),
    ids=lambda value: str(value),
)
@pytest.mark.asyncio
async def test_search_result_id(query, exp_id, api, store_response):
    results = await api.search(query)
    result = [r for r in results if r.title == query.title][0]
    assert result.id == exp_id


@pytest.mark.parametrize(
    argnames=('query', 'exp_directors'),
    argvalues=(
        (Query('The Blues Brothers', year=1980, type=ReleaseType.movie), ('John Landis',)),
        (Query('Deadwood', year=2004, type=ReleaseType.series), ()),
    ),
    ids=lambda value: str(value),
)
@pytest.mark.asyncio
async def test_search_result_directors(query, exp_directors, api, store_response):
    results = await api.search(query)
    assert await results[0].directors() == exp_directors


@pytest.mark.parametrize(
    argnames=('query', 'exp_genres'),
    argvalues=(
        (Query('The Blues Brothers', year=1980, type=ReleaseType.movie), ('music', 'comedy', 'action', 'crime')),
        (Query('February', year=2017, type=ReleaseType.movie), ('drama',)),
        (Query('Deadwood', year=2004, type=ReleaseType.series), ('crime', 'western')),
        (Query('Farang', year=2017, type=ReleaseType.series), ('drama',)),
    ),
    ids=lambda value: str(value),
)
@pytest.mark.asyncio
async def test_search_result_genres(query, exp_genres, api, store_response):
    results = await api.search(query)
    result = [r for r in results if r.title == query.title][0]
    genres = await result.genres()
    if exp_genres:
        for kw in exp_genres:
            assert kw in genres
    else:
        assert not genres


@pytest.mark.parametrize(
    argnames=('query', 'exp_summary'),
    argvalues=(
        (Query('The Blues Brothers', year=1980, type=ReleaseType.movie), 'released from prison'),
        (Query('February', year=2017, type=ReleaseType.movie), 'Husband and wife are going to their vacation cottage to overcome marriage crises'),
        (Query('Deadwood', year=2004, type=ReleaseType.series), 'woven around actual historic events'),
        (Query('Lost & Found Music Studios', year=2015, type=ReleaseType.series), 'singers-songwriters in an elite music program form bonds of friendship'),
        (Query('January', year=1973, type=ReleaseType.movie), ''),
    ),
    ids=lambda value: str(value),
)
@pytest.mark.asyncio
async def test_search_result_summary(query, exp_summary, api, store_response):
    results = await api.search(query)
    result = [r for r in results if r.title == query.title][0]
    summary = await result.summary()
    if exp_summary:
        assert exp_summary in summary
    else:
        assert summary == ''


@pytest.mark.parametrize(
    argnames=('query', 'exp_title'),
    argvalues=(
        (Query('Blues Brothers', year=1980, type=ReleaseType.movie), 'The Blues Brothers'),
        (Query('February', year=2017, type=ReleaseType.movie), "The Blackcoat's Daughter"),
        (Query('Seytan goz qabaginda', year=1987, type=ReleaseType.movie), 'The Devil under the Windshield'),
    ),
    ids=lambda value: str(value),
)
@pytest.mark.asyncio
async def test_search_result_title(query, exp_title, api, store_response):
    results = await api.search(query)
    titles = [r.title for r in results]
    assert exp_title in titles


@pytest.mark.parametrize(
    argnames=('query', 'exp_title_english'),
    argvalues=(
        (Query('The Blues Brothers', year=1980, type=ReleaseType.movie), ''),
        (Query('Deadwood', year=2004, type=ReleaseType.series), ''),
        (Query('Le dolci signore', year=1968, type=ReleaseType.movie), 'Anyone Can Play'),
    ),
    ids=lambda value: str(value),
)
@pytest.mark.asyncio
async def test_search_result_title_english(query, exp_title_english, api, store_response):
    results = await api.search(query)
    assert await results[0].title_english() == exp_title_english


@pytest.mark.parametrize(
    argnames=('query', 'exp_title_original'),
    argvalues=(
        (Query('The Blues Brothers', year=1980, type=ReleaseType.movie), 'The Blues Brothers'),
        (Query('Deadwind', year=2018, type=ReleaseType.series), 'Karppi'),
        (Query('Anyone Can Play', year=1968, type=ReleaseType.movie), 'Le dolci signore'),
    ),
    ids=lambda value: str(value),
)
@pytest.mark.asyncio
async def test_search_result_title_original(query, exp_title_original, api, store_response):
    results = await api.search(query)
    assert await results[0].title_original() == exp_title_original


@pytest.mark.parametrize(
    argnames=('query', 'exp_type'),
    argvalues=(
        (Query('The Blues Brothers', year=1980, type=ReleaseType.movie), ReleaseType.movie),
        (Query('February', year=2017, type=ReleaseType.movie), ReleaseType.movie),
        (Query('Deadwood', year=2004, type=ReleaseType.series), ReleaseType.series),
    ),
    ids=lambda value: str(value),
)
@pytest.mark.asyncio
async def test_search_result_type(query, exp_type, api, store_response):
    results = await api.search(query)
    results_dict = {r.title: r for r in results}
    assert results_dict[query.title].type == exp_type


@pytest.mark.parametrize(
    argnames=('query', 'exp_url'),
    argvalues=(
        (Query('The Blues Brothers', year=1980, type=ReleaseType.movie), 'http://themoviedb.org/movie/525'),
        (Query('February', year=2017, type=ReleaseType.movie), 'http://themoviedb.org/movie/700711'),
        (Query('Deadwood', year=2004, type=ReleaseType.series), 'http://themoviedb.org/tv/1406'),
    ),
    ids=lambda value: str(value),
)
@pytest.mark.asyncio
async def test_search_result_url(query, exp_url, api, store_response):
    results = await api.search(query)
    results_urls = [r.url for r in results]
    assert exp_url in results_urls


@pytest.mark.parametrize(
    argnames=('query', 'exp_title', 'exp_year'),
    argvalues=(
        (Query('Blues Brothers', year=1980, type=ReleaseType.movie), 'The Blues Brothers', '1980'),
        (Query('February', year=2017, type=ReleaseType.movie), "The Blackcoat's Daughter", '2017'),
        (Query('Deadwood', year=2004, type=ReleaseType.series), 'Deadwood', '2004'),
    ),
    ids=lambda value: str(value),
)
@pytest.mark.asyncio
async def test_search_result_year(query, exp_title, exp_year, api, store_response):
    results = await api.search(query)
    results_dict = {r.title: r for r in results}
    assert results_dict[exp_title].year == exp_year

@pytest.mark.asyncio
async def test_search_result_parser_failure(api):
    result = tmdb._TmdbSearchResult(tmdb_api=api)
    assert result.id == ''
    assert result.title == ''
    assert result.type == ReleaseType.unknown
    assert result.url == ''
    assert result.year == ''
    assert await result.cast() == ()
    assert await result.countries() == ()
    assert await result.directors() == ()
    assert await result.genres() == ()
    assert await result.summary() == ''
    assert await result.title_english() == ''
    assert await result.title_original() == ''


@pytest.mark.parametrize(
    argnames=('id', 'exp_cast'),
    argvalues=(
        ('movie/525', (('Dan Aykroyd', 'http://themoviedb.org/person/707-dan-aykroyd'),
                       ('John Belushi', 'http://themoviedb.org/person/7171-john-belushi'))),
        ('movie/334536', (('Emma Roberts', 'http://themoviedb.org/person/34847-emma-roberts'),
                          ('Kiernan Shipka', 'http://themoviedb.org/person/934289-kiernan-shipka'))),
        ('tv/1406', (('Timothy Olyphant', 'http://themoviedb.org/person/18082-timothy-olyphant'),
                     ('Ian McShane', 'http://themoviedb.org/person/6972-ian-mcshane'))),
        ('tv/74802', (('Pihla Viitala', 'http://themoviedb.org/person/93564-pihla-viitala'),
                      ('Lauri Tilkanen', 'http://themoviedb.org/person/124867-lauri-tilkanen'))),
        (None, ()),
    ),
    ids=lambda value: str(value),
)
@pytest.mark.asyncio
async def test_cast(id, exp_cast, api, store_response):
    cast = (await api.cast(id))[:2]
    if not cast:
        assert exp_cast == ()
    else:
        for person, (name, url) in zip_longest(cast, exp_cast):
            assert person == name
            assert person.url == url


@pytest.mark.parametrize(argnames='id', argvalues=('movie/525', 'movie/334536', 'tv/1406', 'tv/74802'))
@pytest.mark.asyncio
async def test_countries(id, api, store_response):
    countries = await api.countries(id)
    assert countries == ()


@pytest.mark.parametrize(
    argnames=('id', 'exp_creators'),
    argvalues=(
        ('movie/125244', ()),
        ('movie/334536', ()),
        ('tv/1406', (('David Milch', 'http://themoviedb.org/person/151295-david-milch'),)),
        ('tv/74802', (('Rike Jokela', 'http://themoviedb.org/person/140497-rike-jokela'),)),
        (None, ()),
    ),
    ids=lambda value: str(value),
)
@pytest.mark.asyncio
async def test_creators(id, exp_creators, api, store_response):
    creators = await api.creators(id)
    if not creators:
        assert exp_creators == ()
    else:
        for person, (name, url) in zip_longest(creators, exp_creators):
            assert person == name
            assert person.url == url


@pytest.mark.parametrize(
    argnames=('id', 'exp_directors'),
    argvalues=(
        ('movie/125244', (('James Algar', 'http://themoviedb.org/person/5690-james-algar'),)),
        ('movie/334536', (('Osgood Perkins', 'http://themoviedb.org/person/90609-osgood-perkins'),)),
        ('tv/1406', ()),
        ('tv/74802', ()),
        (None, ()),
    ),
    ids=lambda value: str(value),
)
@pytest.mark.asyncio
async def test_directors(id, exp_directors, api, store_response):
    directors = await api.directors(id)
    if not directors:
        assert exp_directors == ()
    else:
        for person, (name, url) in zip_longest(directors, exp_directors):
            assert person == name
            assert person.url == url


@pytest.mark.parametrize(
    argnames=('id', 'exp_genres'),
    argvalues=(
        ('movie/525', ('music', 'comedy', 'action', 'crime')),
        ('movie/334536', ('horror', 'thriller')),
        ('tv/1406', ('crime', 'western')),
        ('tv/74802', ('drama', 'crime')),
        ('movie/773336', ('science fiction', 'short')),
        (None, ()),
    ),
    ids=lambda value: str(value),
)
@pytest.mark.asyncio
async def test_genres(id, exp_genres, api, store_response):
    genres = await api.genres(id)
    if exp_genres:
        for member in exp_genres:
            assert member in genres
    else:
        assert not genres


@pytest.mark.parametrize(
    argnames='id, exp_url',
    argvalues=(
        # The Blues Brothers
        ('movie/525', 'https://media.themoviedb.org/t/p/w300_and_h450_bestv2/rhYJKOt6UrQq7JQgLyQcSWW5R86.jpg'),
        # The Blackcoat's Daughter
        ('movie/334536', 'https://media.themoviedb.org/t/p/w300_and_h450_bestv2/zvcdDfwxn0F3Rky3m3Dl2eSVX5X.jpg'),
        # Deadwood
        ('tv/1406', 'https://media.themoviedb.org/t/p/w300_and_h450_bestv2/4Yp35DVbVOAWkfQUIQ7pbh3u0aN.jpg'),
        # Karppi
        ('tv/74802', 'https://media.themoviedb.org/t/p/w300_and_h450_bestv2/cUKqWS2v7D6DVKQze2Iz2netwRH.jpg'),
        # Lost & Found Music Studios
        ('tv/66260', 'https://media.themoviedb.org/t/p/w300_and_h450_bestv2/2febzBrLWIQ9oAlZAvnm4XN0cu1.jpg'),
        # Le dolci signore
        ('movie/3405', 'https://media.themoviedb.org/t/p/w300_and_h450_bestv2/sf31ob8bHZsgCH01J8PutaOnaTA.jpg'),
        (None, ''),
    ),
    ids=lambda value: str(value),
)
@pytest.mark.asyncio
async def test_poster_url(id, exp_url, api, store_response):
    poster_url = await api.poster_url(id)
    assert poster_url == exp_url


@pytest.mark.parametrize(
    argnames=('id', 'exp_runtimes'),
    argvalues=(
        # The Blues Brothers
        ('movie/525', {'default': 133}),
        # The Blackcoat's Daughter
        ('movie/334536', {'default': 93}),
        # Deadwood
        ('tv/1406', {}),
        # Karppi
        ('tv/74802', {}),
        # Lost & Found Music Studios
        ('tv/66260', {}),
        # Le dolci signore
        ('movie/3405', {'default': 88}),
        ('tv/111086', {}),  # no runtimes found
        (None, {}),
    ),
    ids=lambda value: str(value),
)
@pytest.mark.asyncio
async def test_runtimes(id, exp_runtimes, api, store_response):
    runtimes = await api.runtimes(id)
    assert runtimes == exp_runtimes


@pytest.mark.parametrize(
    argnames=('id', 'exp_rating'),
    argvalues=(
        # The Blues Brothers
        ('movie/525', 77.0),
        # The Blackcoat's Daughter
        ('movie/334536', 58.0),
        # Deadwood
        ('tv/1406', 81.0),
        # Karppi
        ('tv/74802', 69.0),
        # Lost & Found Music Studios
        ('tv/66260', 82.0),
        # Le dolci signore
        ('movie/3405', 39.0),
        (None, None),
    ),
    ids=lambda value: str(value),
)
@pytest.mark.asyncio
async def test_rating(id, exp_rating, api, store_response):
    rating = await api.rating(id)
    assert rating == exp_rating


@pytest.mark.parametrize(
    argnames=('id', 'exp_summary'),
    argvalues=(
        ('movie/525', 'released from prison'),
        ('movie/334536', 'Two young students at a prestigious prep school for girls'),
        ('tv/1406', 'woven around actual historic events'),
        ('tv/74802', 'the body of a young woman on a construction site'),
        ('tv/66260', ''),
        ('movie/3405', ''),
        (None, ''),
    ),
    ids=lambda value: str(value),
)
@pytest.mark.asyncio
async def test_summary(id, exp_summary, api, store_response):
    summary = await api.summary(id)
    assert exp_summary in summary


@pytest.mark.parametrize(
    argnames=('id', 'exp_title_english', 'exp_title_original'),
    argvalues=(
        ('movie/221437', '', 'Miss ZOMBIE'),
        ('movie/11841', 'The 36th Chamber of Shaolin', '少林三十六房'),
        ('movie/334536', '', "The Blackcoat's Daughter"),
        ('movie/3405', 'Anyone Can Play', 'Le dolci signore'),
        ('movie/525', '', 'The Blues Brothers'),
        ('movie/22156', 'The Nest', 'Nid de guêpes'),
        ('tv/1406', '', 'Deadwood'),
        ('tv/66260', '', 'Lost & Found Music Studios'),
        ('tv/74802', 'Deadwind', 'Karppi'),
        (None, '', ''),
    ),
    ids=lambda value: str(value),
)
@pytest.mark.asyncio
async def test_title_english_original(id, exp_title_english, exp_title_original, api, store_response):
    assert await api.title_original(id) == exp_title_original
    assert await api.title_english(id) == exp_title_english
    assert await api.title_english(id, default_to_original=False) == exp_title_english
    if exp_title_english:
        assert await api.title_english(id, default_to_original=True) == exp_title_english
    else:
        assert await api.title_english(id, default_to_original=True) == exp_title_original


@pytest.mark.parametrize(
    argnames=('id', 'exp_type'),
    argvalues=(
        ('movie/525', ReleaseType.movie),
        ('tv/525', ReleaseType.series),
        ('tv/1406', ReleaseType.series),
        ('movie/1406', ReleaseType.movie),
        (None, ReleaseType.unknown),
    ),
    ids=lambda value: str(value),
)
@pytest.mark.asyncio
async def test_type(id, exp_type, api, store_response):
    type = await api.type(id)
    assert type is exp_type


@pytest.mark.parametrize(
    argnames=('id', 'exp_url'),
    argvalues=(
        ('movie/525', f'{tmdb.TmdbApi._url_base}/movie/525'),
        ('/tv/1406', f'{tmdb.TmdbApi._url_base}/tv/1406'),
        (None, ''),
    ),
    ids=lambda value: str(value),
)
@pytest.mark.asyncio
async def test_url(id, exp_url, api):
    assert await api.url(id) == exp_url


@pytest.mark.parametrize(
    argnames=('id', 'exp_year'),
    argvalues=(
        ('movie/525', '1980'),
        ('movie/334536', '2017'),
        ('tv/1406', '2004'),
        ('tv/74802', '2018'),
        (None, ''),
    ),
    ids=lambda value: str(value),
)
@pytest.mark.asyncio
async def test_year(id, exp_year, api, store_response):
    assert await api.year(id) == exp_year
