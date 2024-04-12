import collections
import copy
import itertools
import pickle
import re

import pytest

from upsies.utils import imghosts, types


@pytest.mark.parametrize(
    argnames='value, exp_int',
    argvalues=(
        ('1', 1), ('-1', -1),
        ('0.1', 0), ('-0.1', 0),
        ('0.9', 0), ('-0.9', 0),
        ('100', 100), (100, 100), (100.0, 100),
    ),
)
def test_Integer_valid_values(value, exp_int):
    i = types.Integer(value)
    assert i == exp_int

@pytest.mark.parametrize(
    argnames='value',
    argvalues=('zero', 'foo'),
)
def test_Integer_invalid_values(value):
    with pytest.raises(ValueError, match=rf'^Invalid integer value: {value!r}$'):
        types.Integer(value)

def test_Integer_min_max_values():
    min = 0
    max = 10

    with pytest.raises(ValueError, match=rf'^Minimum is {min}$'):
        types.Integer(min - 1, min=min, max=max)
    with pytest.raises(ValueError, match=rf'^Maximum is {max}$'):
        types.Integer(max + 1, min=min, max=max)

    for value in range(min, max + 1):
        i = types.Integer(value, min=min, max=max)
        assert i == value

    i = types.Integer(min, min=min, max=max)
    assert i.min == min
    assert i.max == max

    with pytest.raises(ValueError, match=rf'^Minimum is {min}$'):
        type(i)(min - 1)
    with pytest.raises(ValueError, match=rf'^Maximum is {max}$'):
        type(i)(max + 1)

@pytest.mark.parametrize(
    argnames='value, min, max, exp_repr',
    argvalues=(
        (5, 0, 10, 'Integer(5, min=0, max=10)'),
        (5, 0, None, 'Integer(5, min=0)'),
        (5, None, 10, 'Integer(5, max=10)'),
    ),
)
def test_Integer_repr(value, min, max, exp_repr):
    i = types.Integer(value, min=min, max=max)
    assert repr(i) == exp_repr

def test_Integer_str():
    i = types.Integer(3, min=0, max=10)
    assert str(i) == '3'


@pytest.mark.parametrize(
    argnames='value, options',
    argvalues=(
        ('1', (1, 2, 3, 4)),
        (2, (1, 2, 3, 4)),
        (3, ('1', '2', '3', '4')),
        ('4', ('1', '2', '3', '4')),
    ),
)
def test_Choice_valid_values(value, options):
    choice = types.Choice(value, options)
    assert choice == str(choice)
    assert isinstance(choice, str)

@pytest.mark.parametrize(
    argnames='empty_ok, error_expected',
    argvalues=(
        (False, True),
        (True, False),
    ),
)
def test_Choice_empty_ok(empty_ok, error_expected):
    if error_expected:
        with pytest.raises(ValueError, match=r'^Not one of bar, foo: $'):
            types.Choice('', options=('foo', 'bar'), empty_ok=empty_ok)
    else:
        choice = types.Choice('', options=('foo', 'bar'), empty_ok=empty_ok)
        assert choice == ''

@pytest.mark.parametrize(
    argnames='case_sensitive, value, options, error_expected',
    argvalues=(
        (False, 'foo', ('foo', 'bar', 'baz'), False),
        (True, 'foo', ('foo', 'bar', 'baz'), False),
        (False, 'Foo', ('foo', 'bar', 'baz'), False),
        (True, 'Foo', ('foo', 'bar', 'baz'), True),
        (False, 'foo', ('Foo', 'Bar', 'Baz'), False),
        (True, 'foo', ('Foo', 'Bar', 'Baz'), True),
        (False, 'Foo', ('Foo', 'Bar', 'Baz'), False),
        (True, 'Foo', ('Foo', 'Bar', 'Baz'), False),
    ),
)
def test_Choice_case_sensitive(case_sensitive, value, options, error_expected):
    if error_expected:
        options_str = ', '.join(sorted(options))
        with pytest.raises(ValueError, match=rf'^Not one of {options_str}: {value}$'):
            types.Choice(value, options=options, case_sensitive=case_sensitive)
    else:
        choice = types.Choice(value, options=options, case_sensitive=case_sensitive)
        assert choice == value

@pytest.mark.parametrize(
    argnames='value, options, exp_error',
    argvalues=(
        (0, (1, 2, 3, 4), 'Not one of 1, 2, 3, 4: 0'),
        ('foo', (1, 2, 3, 4), 'Not one of 1, 2, 3, 4: foo'),
    ),
)
def test_Choice_invalid_values(value, options, exp_error):
    with pytest.raises(ValueError, match=rf'^{re.escape(exp_error)}$'):
        types.Choice(value, options)

    choice = types.Choice(options[0], options)
    with pytest.raises(ValueError, match=rf'^{re.escape(exp_error)}$'):
        type(choice)(value)

def test_Choice_repr():
    choice = types.Choice('bar', options=('foo', 'bar', 'baz'))
    assert repr(choice) == "Choice('bar', options=('bar', 'baz', 'foo'))"


@pytest.mark.parametrize('valid_image_host_name', imghosts.imghost_names())
@pytest.mark.parametrize(
    argnames='mutilator',
    argvalues=(
        None,
        str.upper,
        str.capitalize,
    ),
)
def test_ImageHost_valid_values(valid_image_host_name, mutilator):
    mutilated_name = (
        mutilator(valid_image_host_name)
        if mutilator else
        valid_image_host_name
    )
    cls = types.ImageHost()
    name = cls(mutilated_name)
    assert name == mutilated_name
    assert isinstance(name, cls)
    assert isinstance(name, str)

def test_ImageHost_invalid_value():
    valid_names = ', '.join(imghosts.imghost_names())
    with pytest.raises(ValueError, match=rf'^Not one of {valid_names}: foo$'):
        types.ImageHost()('foo')

@pytest.mark.parametrize('is_running_in_development_environment', (True, False), ids=('developing', 'not developing'))
@pytest.mark.parametrize(
    argnames='imghost_names, allowed, disallowed, exp_options',
    argvalues=(
        pytest.param(
            ('foo', 'bar', 'baz'),
            None,
            None,
            ('foo', 'bar', 'baz'),
            id='default allowed, default disallowed',
        ),
        pytest.param(
            ('foo', 'bar', 'baz'),
            ('foo', 'bar'),
            None,
            ('foo', 'bar'),
            id='some allowed, default disallowed',
        ),
        pytest.param(
            ('foo', 'bar', 'baz'),
            None,
            ('bar', 'baz'),
            ('foo',),
            id='default allowed, some disallowed',
        ),
        pytest.param(
            ('foo', 'bar', 'baz'),
            ('foo', 'bar'),
            ('baz',),
            ('foo', 'bar'),
            id='some allowed, some disallowed',
        ),
    ),
    ids=lambda v: repr(v),
)
def test_ImageHost_allowed_and_disallowed(
        imghost_names, allowed, disallowed, is_running_in_development_environment,
        exp_options,
        mocker,
):
    mocker.patch('upsies.utils.imghosts.imghost_names', return_value=imghost_names)
    mocker.patch('upsies.utils.is_running_in_development_environment', return_value=is_running_in_development_environment)
    cls = types.ImageHost(allowed=allowed, disallowed=disallowed)
    if is_running_in_development_environment:
        exp_options = set(exp_options)
    exp_options = sorted(exp_options)
    with pytest.raises(ValueError, match=rf'^Not one of {", ".join(exp_options)}: asdf$'):
        cls('asdf')


@pytest.mark.parametrize(
    argnames='string, exp_bool',
    argvalues=(
        ('true', True), ('false', False),
        ('yes', True), ('no', False),
        ('1', True), ('0', False),
        ('on', True), ('off', False),
        ('aye', True), ('nay', False),
    ),
)
def test_Bool_valid_values(string, exp_bool):
    bool = types.Bool(string)
    if exp_bool:
        assert bool
    else:
        assert not bool
    assert str(bool) == string

@pytest.mark.parametrize(
    argnames='string',
    argvalues=('da', 'nyet'),
)
def test_Bool_invalid_values(string):
    with pytest.raises(ValueError, match=rf'^Invalid boolean value: {string!r}$'):
        types.Bool(string)

@pytest.mark.parametrize(
    argnames='a, b',
    argvalues=(
        (types.Bool('yes'), types.Bool('true')),
        (types.Bool('yes'), True),
        (types.Bool('yes'), 'yes'),
        (types.Bool('no'), 'no'),
    ),
)
def test_Bool_equality(a, b):
    assert a == b
    assert b == a
    assert not (a != b)
    assert not (b != a)

@pytest.mark.parametrize(
    argnames='a, b',
    argvalues=(
        (types.Bool('yes'), types.Bool('false')),
        (types.Bool('no'), types.Bool('true')),
        (types.Bool('yes'), False),
        (types.Bool('no'), True),
        (types.Bool('yes'), 'no'),
        (types.Bool('no'), 'yes'),
        (types.Bool('yes'), 0),
        (types.Bool('no'), 0),
        (types.Bool('yes'), ''),
        (types.Bool('no'), ''),
    ),
)
def test_Bool_inequality(a, b):
    assert a != b
    assert b != a
    assert not (a == b)
    assert not (b == a)

def test_Bool_attributes():
    assert types.Bool.truthy == ('true', 'yes', '1', 'on', 'aye')
    assert types.Bool.falsy == ('false', 'no', '0', 'off', 'nay')

@pytest.mark.parametrize(
    argnames='value, exp_repr',
    argvalues=(
        tuple(
            itertools.chain(
                ((value, f'Bool({value!r})') for value in types.Bool.truthy),
                ((value, f'Bool({value!r})') for value in types.Bool.falsy),
                ((value.title(), f'Bool({value.title()!r})') for value in types.Bool.truthy),
                ((value.title(), f'Bool({value.title()!r})') for value in types.Bool.falsy),
            ),
        )
    ),
)
def test_Bool___repr__(value, exp_repr):
    assert repr(types.Bool(value)) == exp_repr


@pytest.mark.parametrize('number', ('0', '1', '10', '11.5', '11.05', '99', '9999'))
@pytest.mark.parametrize('space', ('', ' '))
@pytest.mark.parametrize(
    argnames='prefix, multiplier',
    argvalues=(
        ('', 1),
        ('k', 1000),
        ('M', 1000**2),
        ('G', 1000**3),
        ('T', 1000**4),
        ('P', 1000**5),
        ('Ki', 1024),
        ('Mi', 1024**2),
        ('Gi', 1024**3),
        ('Ti', 1024**4),
        ('Pi', 1024**5),
    ),
)
@pytest.mark.parametrize('unit', ('', 'B'))
def test_Bytes_from_valid_string(number, space, prefix, multiplier, unit):
    bytes = types.Bytes(f'{number}{space}{prefix}{unit}')
    assert bytes == int(float(number) * multiplier)

@pytest.mark.parametrize(
    argnames='string, exp_msg',
    argvalues=(
        ('foo', 'Invalid size: foo'),
        ('10x', 'Invalid unit: x'),
        ('10kx', 'Invalid unit: kx'),
        ('10 Mx', 'Invalid unit: Mx'),
    ),
)
def test_Bytes_from_invalid_string(string, exp_msg):
    with pytest.raises(ValueError, match=rf'^{exp_msg}$'):
        types.Bytes(string)

@pytest.mark.parametrize(
    argnames='number, exp_string',
    argvalues=(
        (0, '0 B'),
        (1, '1 B'),
        (10, '10 B'),
        (999, '999 B'),
        (1000, '1 kB'),
        (1001, '1 kB'),
        (1000 * 1.5, '1.5 kB'),
        (1000 * 1.75, '1.75 kB'),
        (1000 * 1.799, '1.8 kB'),
        (1023, '1023 B'),
        (1024, '1 KiB'),
        (1025, '1 KiB'),
        (1024 * 1.5, '1.5 KiB'),
        (1024 * 1.75, '1.79 kB'),
        (1024 * 1.799, '1.8 KiB'),
        (1000**2, '1 MB'), (1000**3, '1 GB'), (1000**4, '1 TB'), (1000**5, '1 PB'),
        (1024**2, '1 MiB'), (1024**3, '1 GiB'), (1024**4, '1 TiB'), (1024**5, '1 PiB'),
    ),
)
def test_Bytes_as_string(number, exp_string):
    string = str(types.Bytes(number))
    assert string == exp_string

@pytest.mark.parametrize(
    argnames='number, decimal_places, prefix, trailing_zeros, exp_result',
    argvalues=(
        (0, 0, 'binary', True, '0 B'),
        (0, 0, 'decimal', False, '0 B'),
        (0, 1, 'binary', False, '0 B'),
        (0, 1, 'decimal', True, '0.0 B'),

        (1, 0, 'binary', True, '1 B'),
        (1, 0, 'decimal', False, '1 B'),
        (1, 3, 'binary', False, '1 B'),
        (1, 3, 'decimal', True, '1.000 B'),

        (999, 3, 'decimal', True, '999.000 B'),
        (1001, 3, 'decimal', True, '1.001 kB'),
        (1001, 4, 'decimal', True, '1.0010 kB'),
        (1001, 4, 'decimal', False, '1.001 kB'),

        (999, 3, 'binary', False, '999 B'),
        (1000, 2, 'binary', False, '1000 B'),
        (1000, 2, 'binary', True, '1000.00 B'),
        (1001, 1, 'binary', True, '1001.0 B'),

        (1024, 4, 'decimal', True, '1.0240 kB'),
        (1024, 3, 'decimal', True, '1.024 kB'),
        (1024, 2, 'decimal', True, '1.02 kB'),
        (1024, 1, 'decimal', True, '1.0 kB'),
        (1024, 1, 'decimal', False, '1 kB'),
        (1024, 0, 'decimal', True, '1 kB'),

        (1023, 0, 'binary', True, '1023 B'),
        (1023, 1, 'binary', True, '1023.0 B'),
        (1023, 1, 'binary', False, '1023 B'),

        (1024, 1, 'binary', True, '1.0 KiB'),
        (1024, 1, 'binary', False, '1 KiB'),
        (1024, 0, 'binary', True, '1 KiB'),

        (1025, 5, 'binary', True, '1.00098 KiB'),
        (1025, 4, 'binary', True, '1.0010 KiB'),
        (1025, 4, 'binary', False, '1.001 KiB'),
        (1025, 3, 'binary', True, '1.001 KiB'),
        (1025, 2, 'binary', True, '1.00 KiB'),
        (1025, 2, 'binary', False, '1 KiB'),

        (4000, 2, 'shortest', False, '4 kB'),
        (4096, 2, 'shortest', False, '4 KiB'),

        (100 * 1e6, 0, 'decimal', False, '100 MB'),
        (100, 3, 'foo', False, ValueError("Invalid prefix: 'foo'")),
    ),
)
def test_Bytes_format(number, prefix, decimal_places, trailing_zeros, exp_result):
    if isinstance(exp_result, Exception):
        with pytest.raises(type(exp_result), match=rf'^{re.escape(str(exp_result))}$'):
            types.Bytes(number).format(
                prefix=prefix,
                decimal_places=decimal_places,
                trailing_zeros=trailing_zeros,
            )
    else:
        string = types.Bytes(number).format(
            prefix=prefix,
            decimal_places=decimal_places,
            trailing_zeros=trailing_zeros,
        )
        assert string == exp_result

def test_Bytes_repr():
    b = types.Bytes(123)
    assert repr(b) == 'Bytes(123)'


@pytest.mark.parametrize(
    argnames=('name', 'bool_value'),
    argvalues=(
        ('movie', True),
        ('series', True),
        ('season', True),
        ('episode', True),
        ('unknown', False),
    ),
)
def test_ReleaseType_truthiness(name, bool_value):
    assert bool(getattr(types.ReleaseType, name)) is bool_value

@pytest.mark.parametrize(
    argnames=('name', 'exp_str'),
    argvalues=(
        ('movie', 'movie'),
        ('season', 'season'),
        ('series', 'season'),
        ('episode', 'episode'),
        ('unknown', 'unknown'),
    ),
)
def test_ReleaseType_string(name, exp_str):
    assert str(getattr(types.ReleaseType, name)) == exp_str

@pytest.mark.parametrize(
    argnames=('name', 'exp_repr'),
    argvalues=(
        ('movie', 'ReleaseType.movie'),
        ('season', 'ReleaseType.season'),
        ('series', 'ReleaseType.season'),
        ('episode', 'ReleaseType.episode'),
        ('unknown', 'ReleaseType.unknown'),
    ),
)
def test_ReleaseType_repr(name, exp_repr):
    assert repr(getattr(types.ReleaseType, name)) == exp_repr


@pytest.mark.parametrize(
    argnames=('name', 'bool_value'),
    argvalues=(
        ('true', True),
        ('false', False),
        ('renamed', False),
        ('altered', False),
        ('unknown', False),
    ),
)
def test_SceneCheckResult_truthiness(name, bool_value):
    assert bool(getattr(types.SceneCheckResult, name)) is bool_value

@pytest.mark.parametrize(
    argnames=('name', 'exp_str'),
    argvalues=(
        ('true', 'true'),
        ('false', 'false'),
        ('renamed', 'renamed'),
        ('altered', 'altered'),
        ('unknown', 'unknown'),
    ),
)
def test_SceneCheckResult_string(name, exp_str):
    assert str(getattr(types.SceneCheckResult, name)) == exp_str

@pytest.mark.parametrize(
    argnames=('name', 'exp_repr'),
    argvalues=(
        ('true', 'SceneCheckResult.true'),
        ('false', 'SceneCheckResult.false'),
        ('renamed', 'SceneCheckResult.renamed'),
        ('altered', 'SceneCheckResult.altered'),
        ('unknown', 'SceneCheckResult.unknown'),
    ),
)
def test_SceneCheckResult_repr(name, exp_repr):
    assert repr(getattr(types.SceneCheckResult, name)) == exp_repr


@pytest.mark.parametrize(
    argnames=('pattern, exp_result, string, exp_groups'),
    argvalues=(
        (r'(.*) foo(.*)baz$', re.compile(r'(.*) foo(.*)baz$'), 'hey: foo bar baz', ('hey:', ' bar ')),
        (types.RegEx(r'(.*) foo(.*)baz$'), re.compile(r'(.*) foo(.*)baz$'), 'hey: foo bar baz', ('hey:', ' bar ')),
        (r'*foo\.bar$', ValueError(r'*foo\.bar$: Nothing to repeat at position 0'), None, None),
    ),
)
def test_RegEx(pattern, exp_result, string, exp_groups):
    if isinstance(exp_result, Exception):
        with pytest.raises(type(exp_result), match=rf'^{re.escape(str(exp_result))}$'):
            types.RegEx(pattern)
    else:
        # Works like re.Pattern
        regex = types.RegEx(pattern)
        match = regex.search(string)
        assert match.groups() == exp_groups
        assert regex.pattern == exp_result.pattern

        # Better string representations
        assert str(regex) == exp_result.pattern
        assert repr(regex) == f'RegEx({exp_result.pattern!r})'

        # Equality and hashability
        assert regex == types.RegEx(exp_result.pattern)
        assert hash(regex) == hash(types.RegEx(exp_result.pattern))

        # Picklability
        pickled = pickle.dumps(regex)
        assert pickle.loads(pickled) == regex

        # copy.deepcopy()
        copied = copy.deepcopy(regex)
        assert repr(copied) == repr(regex)
        assert id(copied) != id(regex)


@pytest.mark.parametrize(
    argnames=('item_type, default, separator, exp_result, exp___doc__'),
    argvalues=(
        # Multiple values
        (int, ['10', '20', '45'], None, [10, 20, 45], 'Immutable list of int'),
        (int, None, None, [], 'Immutable list of int'),
        (int, ['10', 'foo', '45'], None, ValueError('Invalid value: foo'), None),
        # Single value
        (int, 123, None, [123], 'Immutable list of int'),
        (int, ..., None, ValueError('Invalid value: Ellipsis'), None),
        # Separator
        (str, 'foo,bar', None, ['foo,bar'], 'Immutable list of str'),
        (str, 'foo,bar', ',', ['foo', 'bar'], 'Immutable list of str'),
        (str, 'foo,,bar,baz,,', ',', ['foo', 'bar', 'baz'], 'Immutable list of str'),
        # Special case for re.Pattern because its __str__() behaves like __repr__()
        (types.RegEx, ['(.)'], None, [types.RegEx('(.)')], 'Immutable list of RegEx'),
        (types.RegEx, ['(.'], None, ValueError('Invalid value: (.'), None),
    ),
    ids=lambda v: repr(v),
)
def test_ListOf(item_type, default, separator, exp_result, exp___doc__):
    args = [item_type]
    if default:
        args.append(default)
    kwargs = {}
    if separator is not None:
        kwargs['separator'] = separator

    if isinstance(exp_result, Exception):
        with pytest.raises(type(exp_result), match=rf'^{re.escape(str(exp_result))}$'):
            types.ListOf(*args, **kwargs)
    else:
        list_of = types.ListOf(*args, **kwargs)
        assert list_of == exp_result
        assert isinstance(list_of, collections.abc.Sequence)
        assert not isinstance(list_of, collections.abc.MutableSequence)

        # __doc__
        assert type(list_of).__doc__ == exp___doc__

        # __geitem__()
        for i, exp_item in enumerate(exp_result):
            assert list_of[i] == exp_item

        # __len__()
        assert len(list_of) == len(exp_result)

        # __eq__()
        assert list_of == list_of
        assert list_of == exp_result
        assert list_of == list(exp_result)
        assert list_of == tuple(exp_result)
        unexp_result = exp_result + ['foo']
        if list_of:
            assert list_of != list_of[0:0]
        assert list_of != list(unexp_result)
        assert list_of != tuple(unexp_result)
        assert list_of != 123
        assert list_of != 'hello'

        # __hash__()
        class OtherType(str):
            pass
        if default is None:
            assert hash(list_of) == hash(types.ListOf(list_of.item_type, separator=separator))
            assert hash(list_of) == hash(types.ListOf(list_of.item_type, separator='!'))
            assert hash(list_of) != hash(types.ListOf(OtherType, separator=separator))
        else:
            assert hash(list_of) == hash(types.ListOf(list_of.item_type, separator=separator, default=list_of))
            assert hash(list_of) == hash(types.ListOf(list_of.item_type, separator='!', default=list_of))
            assert hash(list_of) != hash(types.ListOf(OtherType, separator=separator, default=list_of))
        assert hash(list_of) != hash(types.ListOf(list_of.item_type, default=('1', '2', '3'), separator=separator))

        # __str__()
        assert str(list_of) == ', '.join(
            (
                item.pattern
                if isinstance(item, re.Pattern) else
                str(item)
            )
            for item in exp_result
        )

        # __repr__()
        assert repr(list_of) == (
            type(list_of).__name__
            + '('
            + repr(tuple(exp_result))
            + ')'
        )

        # __name__
        assert type(list_of).__name__ == (
            'ListOf'
            + item_type.__name__[0].upper()
            + item_type.__name__[1:]
        )
        assert type(list_of).__qualname__ == type(list_of).__name__


@pytest.mark.parametrize(
    argnames=('string, exp_result'),
    argvalues=(
        ('foo -> bar', ('foo', 'bar')),
        ('foo->bar', ('foo', 'bar')),
        ('  foo  ->   bar  ', ('foo', 'bar')),
        ('-> bar', ValueError('Invalid path translation: -> bar')),
    ),
)
def test_PathTranslation(string, exp_result):
    if isinstance(exp_result, Exception):
        with pytest.raises(type(exp_result), match=rf'^{re.escape(str(exp_result))}$'):
            types.PathTranslation(string)
    else:
        translation = types.PathTranslation(string)
        assert (translation.local, translation.remote) == exp_result

        # __str__()
        assert str(translation) == f'{translation.local} -> {translation.remote}'


@pytest.mark.parametrize(
    argnames=('path, translations, exp_result'),
    argvalues=(
        (
            '/foo/bar/baz',
            types.PathTranslations(),
            '/foo/bar/baz',
        ),
        (
            '/foo/bar/baz',
            types.PathTranslations((
                '/foo/bar/baz -> asdf',
            )),
            'asdf',
        ),
        (
            '/foo/bar/baz',
            types.PathTranslations((
                '/foo/bar/baz/bam -> asdf',
            )),
            '/foo/bar/baz',
        ),
        (
            '/foo/bar/baz',
            types.PathTranslations((
                'oo/ba -> asdf',
            )),
            '/fasdfr/baz',
        ),
    ),
    ids=lambda v: repr(v),
)
def test_PathTranslations(path, translations, exp_result):
    assert translations.translate(path) == exp_result
