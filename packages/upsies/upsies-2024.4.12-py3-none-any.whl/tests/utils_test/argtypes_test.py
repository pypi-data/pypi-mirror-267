import argparse
import pathlib
import re
from unittest.mock import call, patch

import pytest

from upsies import defaults, errors, trackers, utils
from upsies.utils import argtypes


@pytest.mark.parametrize(
    argnames='argtype, values, exp_result',
    argvalues=(
        (int, '\t1, 3 ,,5,  ', [1, 3, 5]),
        (float, '1.2,3.4,5.9', [1.2, 3.4, 5.9]),
        (int, '1, foo, 5', argparse.ArgumentTypeError('Invalid value: foo')),
    ),
    ids=lambda v: repr(v),
)
def test_comma_separated(argtype, values, exp_result):
    func = argtypes.comma_separated(argtype)
    if isinstance(exp_result, Exception):
        with pytest.raises(type(exp_result), match=rf'^{re.escape(str(exp_result))}$'):
            func(values)
    else:
        return_value = func(values)
        assert return_value == exp_result


def test_client_valid_value(mocker):
    mocker.patch('upsies.utils.btclient.client_names', return_value=('foo', 'bar', 'baz'))
    assert argtypes.client('foo') == 'foo'
    assert argtypes.client('Bar') == 'bar'
    assert argtypes.client('BAZ') == 'baz'

def test_client_invalid_value(mocker):
    mocker.patch('upsies.utils.btclient.client_names', return_value=('foo', 'bar', 'baz'))
    with pytest.raises(argparse.ArgumentTypeError, match=r'^Unsupported client: asdf$'):
        argtypes.client('asdf')


def test_content(mocker):
    release_mock = mocker.patch('upsies.utils.argtypes.release', return_value='release/path')
    existing_path_mock = mocker.patch('upsies.utils.argtypes.existing_path', return_value='existing/path')
    assert argtypes.content('given/path') == 'existing/path'
    assert release_mock.call_args_list == [call('given/path')]
    assert existing_path_mock.call_args_list == [call('release/path')]


@pytest.mark.parametrize(
    argnames='path, path_exists, exp_exc',
    argvalues=(
        ('path/to/foo', True, None),
        (pathlib.Path('path/to/foo'), True, None),
        ('path/to/foo', False, argparse.ArgumentTypeError('No such file or directory: path/to/foo')),
    ),
    ids=lambda v: repr(v),
)
def test_existing_path(path, path_exists, exp_exc, mocker):
    exists_mock = mocker.patch('os.path.exists', return_value=path_exists)
    if path_exists:
        assert argtypes.existing_path(path) == str(path)
    else:
        with pytest.raises(type(exp_exc), match=rf'^{re.escape(str(exp_exc))}$'):
            argtypes.content(path)
    assert exists_mock.call_args_list == [call(str(path))]


@pytest.mark.parametrize('imghost', utils.imghosts.imghost_names())
def test_imghost_valid_value(imghost):
    assert argtypes.imghost(imghost) == imghost
    assert argtypes.imghost(imghost.upper()) == imghost
    assert argtypes.imghost(imghost.capitalize()) == imghost

def test_imghost_invalid_value():
    with pytest.raises(argparse.ArgumentTypeError, match=r'^Unsupported image hosting service: foo$'):
        argtypes.imghost('foo')


@pytest.mark.parametrize('imghost', utils.imghosts.imghost_names())
def test_imghosts_only_valid_values(imghost):
    existing_names = utils.imghosts.imghost_names()
    existing_names.insert(0, '')
    existing_names.insert(2, '')
    existing_names.append('')
    existing_names[2] = existing_names[2].upper()
    existing_names_combined = ','.join(existing_names)
    assert argtypes.imghosts(existing_names_combined) == utils.imghosts.imghost_names()

def test_imghosts_invalid_value():
    existing_names = utils.imghosts.imghost_names()
    existing_names.insert(2, 'foo')
    existing_names_combined = ','.join(existing_names)
    with pytest.raises(argparse.ArgumentTypeError, match=r'^Unsupported image hosting service: foo$'):
        argtypes.imghosts(existing_names_combined)


@pytest.mark.parametrize(
    argnames='value, exp_value',
    argvalues=(
        (123, 123),
        (123.2, 123),
        ('123', 123),
        ('123.2', 123),
    ),
    ids=lambda v: repr(v),
)
def test_integer_valid_value(value, exp_value):
    assert argtypes.integer(value) == exp_value

@pytest.mark.parametrize('value', ('one', (1, 2, 3)), ids=lambda v: repr(v))
def test_integer_invalid_value(value):
    with pytest.raises(argparse.ArgumentTypeError, match=rf'^Not an integer: {re.escape(repr(value))}'):
        argtypes.integer(value)


@pytest.mark.parametrize(
    argnames='min, max, value, exp_value',
    argvalues=(
        (1, 5, 5.0, 5),
    ),
)
def test_number_of_screenshots_valid_value(min, max, value, exp_value):
    assert argtypes.number_of_screenshots(min=min, max=max)(value) == exp_value

@pytest.mark.parametrize(
    argnames='min, max, value, exp_error',
    argvalues=(
        (1, 5, 0, 'Minimum is 1'),
        (1, 5, 6, 'Maximum is 5'),
        (1, 5, 'asdf', "Invalid integer value: 'asdf'"),
    ),
)
def test_number_of_screenshots_invalid_value(min, max, value, exp_error):
    with pytest.raises(argparse.ArgumentTypeError, match=rf'^{re.escape(exp_error)}$'):
        argtypes.number_of_screenshots(min=min, max=max)(value)


@pytest.mark.parametrize('option', defaults.option_paths())
def test_option_valid_value(option):
    assert argtypes.option(option) == option

def test_option_invalid_value():
    with pytest.raises(argparse.ArgumentTypeError, match=r'^Unknown option: foo$'):
        argtypes.option('foo')


@pytest.mark.parametrize(
    argnames='values, value, exp_result',
    argvalues=(
        (('foo', 'bar', 'baz'), 'foo', 'foo'),
        (('foo', 'bar', 'baz'), 'bar', 'bar'),
        (('foo', 'bar', 'baz'), 'baz', 'baz'),
        (('foo', 'bar', 'baz'), 'hello', argparse.ArgumentTypeError('Invalid value: hello')),
    ),
    ids=lambda v: repr(v),
)
def test_one_of(values, value, exp_result):
    func = argtypes.one_of(values)
    if isinstance(exp_result, Exception):
        with pytest.raises(type(exp_result), match=rf'^{re.escape(str(exp_result))}$'):
            func(value)
    else:
        assert func(value) == exp_result


@pytest.mark.parametrize(
    argnames='value, exp_regex',
    argvalues=(
        ('foo.*bar', utils.types.RegEx(r'foo.*bar')),
    ),
)
def test_regex_valid_value(value, exp_regex):
    assert argtypes.regex(value) == exp_regex

@pytest.mark.parametrize(
    argnames='regex, exp_msg',
    argvalues=(
        ('foo[bar', 'Unterminated character set at position 3'),
    ),
)
def test_regex_invalid_value(regex, exp_msg):
    msg = f'{regex}: {exp_msg}'
    with pytest.raises(argparse.ArgumentTypeError, match=rf'^{re.escape(msg)}$'):
        argtypes.regex(regex)


@pytest.mark.parametrize(
    argnames='path, exp_path, exc, exp_exc',
    argvalues=(
        ('path/to/foo', 'path/to/foo', None, None),
        (123, '123', None, None),
        ('path/to/foo', 'path/to/foo', errors.SceneAbbreviatedFilenameError('bar'),
         argparse.ArgumentTypeError(errors.SceneAbbreviatedFilenameError('bar'))),
        ('path/to/foo', 'path/to/foo', RuntimeError('baz'), RuntimeError('baz')),
    ),
    ids=lambda v: str(v),
)
def test_release(path, exp_path, exc, exp_exc, mocker):
    mocker.patch('upsies.utils.predbs.assert_not_abbreviated_filename',
                 side_effect=exc)
    if exp_exc:
        with pytest.raises(type(exp_exc), match=rf'^{re.escape(str(exp_exc))}$'):
            argtypes.release(path)
    else:
        assert argtypes.release(path) == exp_path


@pytest.mark.parametrize('predb_name', utils.predbs.predb_names())
def test_predb_name_valid_value(predb_name):
    assert argtypes.predb_name(predb_name) == predb_name
    assert argtypes.predb_name(predb_name.upper()) == predb_name
    assert argtypes.predb_name(predb_name.capitalize()) == predb_name

def test_predb_name_invalid_value():
    with pytest.raises(argparse.ArgumentTypeError, match=r'^Unsupported scene release database: foo$'):
        argtypes.predb_name('foo')


@pytest.mark.parametrize('predb', utils.predbs.predb_names())
def test_predb_valid_value(predb):
    for return_value in (
            argtypes.predb(predb),
            argtypes.predb(predb.upper()),
            argtypes.predb(predb.capitalize()),
    ):
        assert isinstance(return_value, utils.predbs.PredbApiBase)
        assert return_value.name == predb.lower()

def test_predb_invalid_value():
    with pytest.raises(argparse.ArgumentTypeError, match=r'^Unsupported scene release database: foo$'):
        argtypes.predb('foo')


@pytest.mark.parametrize(
    argnames='value, exp_result',
    argvalues=(
        (None, None),
        ('true', True),
        ('false', False),
        ('maybe', argparse.ArgumentTypeError("Invalid boolean value: 'maybe'")),
    ),
)
def test_bool_or_none(value, exp_result):
    if isinstance(exp_result, Exception):
        with pytest.raises(type(exp_result), match=rf'^{re.escape(str(exp_result))}$'):
            argtypes.bool_or_none(value)
    else:
        return_value = argtypes.bool_or_none(value)
        assert return_value == exp_result


@patch('upsies.utils.timestamp.parse')
def test_timestamp_valid_value(parse_mock):
    assert argtypes.timestamp('foo') is parse_mock.return_value
    assert parse_mock.call_args_list == [call('foo')]

@patch('upsies.utils.timestamp.parse')
@pytest.mark.parametrize('exception', (ValueError, TypeError))
def test_timestamp_invalid_value(parse_mock, exception):
    parse_mock.side_effect = exception('Message!')
    with pytest.raises(argparse.ArgumentTypeError, match=r'^Message!$'):
        argtypes.timestamp('foo')


@pytest.mark.parametrize('tracker', trackers.tracker_names())
def test_tracker_valid_value(tracker):
    assert argtypes.tracker(tracker) == tracker
    assert argtypes.tracker(tracker.upper()) == tracker
    assert argtypes.tracker(tracker.capitalize()) == tracker

def test_tracker_invalid_value():
    with pytest.raises(argparse.ArgumentTypeError, match=r'^Unsupported tracker: foo$'):
        argtypes.tracker('foo')


@pytest.mark.parametrize('webdb', utils.webdbs.webdb_names())
def test_webdb_valid_value(webdb):
    assert argtypes.webdb(webdb) == webdb
    assert argtypes.webdb(webdb.upper()) == webdb
    assert argtypes.webdb(webdb.capitalize()) == webdb

def test_webdb_invalid_value():
    with pytest.raises(argparse.ArgumentTypeError, match=r'^Unsupported database: foo$'):
        argtypes.webdb('foo')
