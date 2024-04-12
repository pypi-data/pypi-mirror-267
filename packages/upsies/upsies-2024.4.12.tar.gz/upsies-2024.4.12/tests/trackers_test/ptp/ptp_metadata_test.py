import pytest

from upsies.trackers.ptp import metadata


@pytest.mark.parametrize('text_transformer',(
    lambda text: text,
    str.capitalize,
    str.lower,
    str.upper,
))
@pytest.mark.parametrize(
    argnames='text, exp_type',
    argvalues=(
        ('', None),

        # Feature Film
        ('feature film', 'Feature Film'),
        ('feature-film', 'Feature Film'),
        ('film', 'Feature Film'),
        ('movie', 'Feature Film'),
        ('blockbuster', None),

        # Short Film
        ('short film', 'Short Film'),
        ('short.film', 'Short Film'),
        ('short', 'Short Film'),
        ('long', None),

        # Miniseries
        ('miniseries', 'Miniseries'),
        ('mini-series', 'Miniseries'),
        ('series', 'Miniseries'),
        ('season', 'Miniseries'),
        ('tv', 'Miniseries'),
        ('tv!', None),

        # Stand-up Comedy
        ('stand-upcomedy', 'Stand-up Comedy'),
        ('standupcomedy', 'Stand-up Comedy'),
        ('stand-up-comedy', 'Stand-up Comedy'),
        ('stand-up-comedy', 'Stand-up Comedy'),
        ('stand-up', 'Stand-up Comedy'),
        ('standup', 'Stand-up Comedy'),
        ('comedy', 'Stand-up Comedy'),
        ('domecy', None),

        # Live Performance
        ('live performance', 'Live Performance'),
        ('live-performance', 'Live Performance'),
        ('liveperformance', 'Live Performance'),
        ('live', 'Live Performance'),
        ('performance', 'Live Performance'),
        ('happening', None),

        # Movie Collection
        ('movie collection', 'Movie Collection'),
        ('movie.collection', 'Movie Collection'),
        ('movie-collection', 'Movie Collection'),
        ('collection', 'Movie Collection'),
        ('bundle', None),
    ),
)
def test_types(text, exp_type, text_transformer):
    def matching_type(text):
        for type, regex in metadata.types.items():
            if regex.search(text):
                return type

    assert matching_type(text_transformer(text)) == exp_type


def test_TrumpableReason_members():
    assert list(metadata.TrumpableReason) == [
        metadata.TrumpableReason.NO_ENGLISH_SUBTITLES,
        metadata.TrumpableReason.HARDCODED_SUBTITLES,
    ]


@pytest.mark.parametrize(
    argnames='reason, exp_value',
    argvalues=(
        (metadata.TrumpableReason.NO_ENGLISH_SUBTITLES, 14),
        (metadata.TrumpableReason.HARDCODED_SUBTITLES, 4),
    ),
    ids=lambda v: repr(v),
)
def test_TrumpableReason_value(reason, exp_value):
    assert reason.value == exp_value


@pytest.mark.parametrize(
    argnames='reason, string',
    argvalues=(
        (metadata.TrumpableReason.NO_ENGLISH_SUBTITLES, 'No English Subtitles'),
        (metadata.TrumpableReason.HARDCODED_SUBTITLES, 'Hardcoded Subtitles'),
    ),
    ids=lambda v: repr(v),
)
def test_TrumpableReason_string(reason, string):
    assert str(reason) == string
    assert type(reason).from_string(string) is reason


def test_ArtistImportance_members():
    assert list(metadata.ArtistImportance) == [
        metadata.ArtistImportance.ACTOR,
        metadata.ArtistImportance.DIRECTOR,
        metadata.ArtistImportance.WRITER,
        metadata.ArtistImportance.PRODUCER,
        metadata.ArtistImportance.COMPOSER,
        metadata.ArtistImportance.CINEMATOGRAPHER,
    ]


@pytest.mark.parametrize(
    argnames='importance, exp_value',
    argvalues=(
        (metadata.ArtistImportance.DIRECTOR, 1),
        (metadata.ArtistImportance.WRITER, 2),
        (metadata.ArtistImportance.PRODUCER, 3),
        (metadata.ArtistImportance.COMPOSER, 4),
        (metadata.ArtistImportance.ACTOR, 5),
        (metadata.ArtistImportance.CINEMATOGRAPHER, 6),
    ),
    ids=lambda v: repr(v),
)
def test_ArtistImportance_value(importance, exp_value):
    assert importance.value == exp_value


@pytest.mark.parametrize(
    argnames='importance, string',
    argvalues=(
        (metadata.ArtistImportance.DIRECTOR, 'Director'),
        (metadata.ArtistImportance.WRITER, 'Writer'),
        (metadata.ArtistImportance.PRODUCER, 'Producer'),
        (metadata.ArtistImportance.COMPOSER, 'Composer'),
        (metadata.ArtistImportance.ACTOR, 'Actor'),
        (metadata.ArtistImportance.CINEMATOGRAPHER, 'Cinematographer'),
    ),
    ids=lambda v: repr(v),
)
def test_ArtistImportance_string(importance, string):
    assert str(importance) == string
    assert type(importance).from_string(string) is importance
