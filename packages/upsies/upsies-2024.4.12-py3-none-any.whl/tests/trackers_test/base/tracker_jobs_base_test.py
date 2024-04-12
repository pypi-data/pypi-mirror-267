import builtins
import os
import pathlib
import re
import types
from unittest.mock import AsyncMock, Mock, PropertyMock, call

import pytest

from upsies import errors, utils
from upsies.trackers.base import TrackerJobsBase


@pytest.fixture
def tracker():
    tracker = Mock()
    tracker.configure_mock(
        name='AsdF',
        options={
            'announce' : 'http://foo.bar',
            'source'   : 'AsdF',
            'exclude'  : ('a', 'b'),
        },
    )
    return tracker


@pytest.fixture
def make_TestTrackerJobs(tracker):
    def make_TestTrackerJobs(**kwargs):
        class TestTrackerJobs(TrackerJobsBase):
            jobs_before_upload = PropertyMock()

        default_kwargs = {
            'content_path': '',
            'tracker': tracker,
            'reuse_torrent_path': '',
            'btclient': Mock(),
            'torrent_destination': '',
            'image_hosts': (Mock(),),
            'screenshots_optimization': 'my optimization level',
            'show_poster': 'maybe show poster',
            'common_job_args': {},
        }
        return TestTrackerJobs(**{**default_kwargs, **kwargs})

    return make_TestTrackerJobs


def test_arguments(make_TestTrackerJobs):
    kwargs = {
        'content_path': Mock(),
        'tracker': Mock(),
        'reuse_torrent_path': Mock(),
        'exclude_files': Mock(),
        'btclient': Mock(),
        'torrent_destination': Mock(),
        'image_hosts': (Mock(),),
        'options': {'mock': 'config'},
    }
    tracker_jobs = make_TestTrackerJobs(**kwargs)
    for k, v in kwargs.items():
        assert getattr(tracker_jobs, k) is v


@pytest.mark.parametrize(
    argnames='common_job_args, overload, exp_return_value',
    argvalues=(
        (
            {'home_directory': 'default/home', 'cache_directory': 'default/cache', 'ignore_cache': False},
            {'home_directory': 'overloaded/home'},
            {'home_directory': 'overloaded/home', 'cache_directory': 'default/cache', 'ignore_cache': False},
        ),
        (
            {'home_directory': 'default/home', 'cache_directory': 'default/cache', 'ignore_cache': False},
            {'cache_directory': 'overloaded/cache'},
            {'home_directory': 'default/home', 'cache_directory': 'overloaded/cache', 'ignore_cache': False},
        ),
        # `ignore_cache=False` can only be overloaded if `ignore_cache=True` was
        # not set globally.
        (
            {'home_directory': 'default/home', 'cache_directory': 'default/cache', 'ignore_cache': False},
            {'ignore_cache': True},
            {'home_directory': 'default/home', 'cache_directory': 'default/cache', 'ignore_cache': True},
        ),
        (
            {'home_directory': 'default/home', 'cache_directory': 'default/cache', 'ignore_cache': True},
            {'ignore_cache': False},
            {'home_directory': 'default/home', 'cache_directory': 'default/cache', 'ignore_cache': True},
        ),
        (
            {'home_directory': 'default/home', 'cache_directory': 'default/cache', 'ignore_cache': True},
            {'ignore_cache': True},
            {'home_directory': 'default/home', 'cache_directory': 'default/cache', 'ignore_cache': True},
        ),
    ),
    ids=lambda v: repr(v),
)
def test_common_job_args(common_job_args, overload, exp_return_value, make_TestTrackerJobs):
    tracker_jobs = make_TestTrackerJobs(common_job_args=common_job_args)
    return_value = tracker_jobs.common_job_args(**overload)
    assert return_value == exp_return_value


def test_signals(make_TestTrackerJobs, mocker):
    Signal_mock = mocker.patch('upsies.utils.signal.Signal')
    tracker_jobs = make_TestTrackerJobs()
    assert tracker_jobs.signal is Signal_mock.return_value
    assert Signal_mock.call_args_list == [call('warning', 'error', 'exception')]
    tracker_jobs.warn('foo')
    assert Signal_mock.return_value.emit.call_args_list == [
        call('warning', 'foo'),
    ]
    tracker_jobs.error('bar')
    assert Signal_mock.return_value.emit.call_args_list == [
        call('warning', 'foo'),
        call('error', 'bar'),
    ]
    tracker_jobs.exception('baz')
    assert Signal_mock.return_value.emit.call_args_list == [
        call('warning', 'foo'),
        call('error', 'bar'),
        call('exception', 'baz'),
    ]


def test_imdb(make_TestTrackerJobs):
    tracker_jobs = make_TestTrackerJobs()
    assert isinstance(tracker_jobs.imdb, utils.webdbs.imdb.ImdbApi)

def test_tmdb(make_TestTrackerJobs):
    tracker_jobs = make_TestTrackerJobs()
    assert isinstance(tracker_jobs.tvmaze, utils.webdbs.tvmaze.TvmazeApi)

def test_tvmaze(make_TestTrackerJobs):
    tracker_jobs = make_TestTrackerJobs()
    assert isinstance(tracker_jobs.tvmaze, utils.webdbs.tvmaze.TvmazeApi)


def test_jobs_after_upload(make_TestTrackerJobs, mocker):
    add_torrent_job_mock = mocker.patch('upsies.trackers.base.TrackerJobsBase.add_torrent_job')
    copy_torrent_job_mock = mocker.patch('upsies.trackers.base.TrackerJobsBase.copy_torrent_job')
    tracker_jobs = make_TestTrackerJobs()
    assert tracker_jobs.jobs_after_upload == (
        add_torrent_job_mock,
        copy_torrent_job_mock,
    )


def test_isolated_jobs(make_TestTrackerJobs, mocker):
    tracker_jobs = make_TestTrackerJobs()
    assert tracker_jobs.isolated_jobs == ()


class Job(str):
    def __new__(cls, name, *, prejobs=(), presignals={}):
        self = super().__new__(
            cls,
            f'Job({name!r}, '
            + 'prejobs=' + ', '.join(repr(j.name) for j in prejobs) + ', '
            + 'presignals=' + ', '.join(repr(j.name) for j in presignals) + ', '
        )
        self.name = str(name)
        self.prejobs = tuple(prejobs)
        self.presignals = dict(presignals)
        return self

@pytest.mark.parametrize(
    argnames='jobs, exp_job_names',
    argvalues=(
        pytest.param(
            [
                Job(name='a'),
                Job(name='b'),
                Job(name='c'),
            ],
            ['a', 'b', 'c'],
            id='No dependencies',
        ),

        # NOTE: `...` or `Ellipsis` is a built-in Python singleton. We use it
        #       here to show that we only need the keys/jobs in `presignals` and
        #       the values are ignored.

        pytest.param(
            [
                Job(name='a', prejobs=[
                    Job(name='x', prejobs=[Job(name='1')]),
                    Job(name='y', prejobs=[Job(name='2', prejobs=[Job(name='ɑ')])]),
                    Job(name='c', prejobs=[]),
                ]),
                Job(name='b', prejobs=[
                    Job(name='x', prejobs=[Job(name='1')]),
                    Job(name='z', prejobs=[Job(name='3')]),
                ]),
                Job(name='c', prejobs=[]),

            ],
            ['a', 'x', '1', 'y', '2', 'ɑ', 'c', 'b', 'z', '3'],
            id='Dependencies from prejobs',
        ),

        pytest.param(
            [
                Job(name='a', presignals={Job(name='ɑ'): ...}),
                Job(name='b', presignals={
                    Job(name='x'): ...,
                    Job(name='y', presignals={Job(name='1'): ...}): ...,
                }),
                Job(name='c', presignals={
                    Job(name='y', presignals={Job(name='1'): ...}): ...,
                    Job(name='z', presignals={
                        Job(name='2'): ...,
                        Job(name='3', presignals={Job(name='ɑ'): ...}): ...,
                    }): ...,
                }),
            ],
            ['a', 'ɑ', 'b', 'x', 'y', '1', 'c', 'z', '2', '3'],
            id='Dependencies from presignals',
        ),

        pytest.param(
            [
                Job(name='c', prejobs=[
                    Job(name='z', presignals={
                        Job(name='2'): ...,
                    }),
                ]),
            ],
            ['c', 'z', '2'],
            id='Job depends on prejobs with presignals',
        ),

        pytest.param(
            [
                Job(name='c', presignals={
                    Job(name='z', prejobs=[
                        Job(name='2'),
                    ]): ...,
                }),
            ],
            ['c', 'z', '2'],
            id='Job depends on presignals with prejobs',
        ),

        pytest.param(
            [
                Job(name='a', prejobs=[Job(name='ɑ')], presignals={Job(name='1'): ...}),
                Job(name='b', presignals={
                    Job(name='x'): ...,
                    Job(name='y', prejobs=[Job(name='1')]): ...,
                }),
                Job(name='c', prejobs=[
                    Job(name='y', prejobs=[Job(name='1')]),
                    Job(
                        name='z',
                        prejobs=[Job(name='10'), Job(name='20')],
                        presignals={
                            Job(
                                name='2',
                                presignals={
                                    Job(
                                        name='β',
                                        prejobs=[
                                            Job(name='a', prejobs=[Job(name='ɑ')], presignals={Job(name='1'): ...}),
                                            Job(name='y', prejobs=[Job(name='1')]),
                                        ],
                                    ): ...,
                                },
                            ): ...,
                            Job(
                                name='3',
                                prejobs=[
                                    Job(name='a', prejobs=[Job(name='ɑ')], presignals={Job(name='1'): ...}),
                                ],
                                presignals={
                                    Job(name='a', prejobs=[Job(name='ɑ')], presignals={Job(name='1'): ...}): ...,
                                    Job(name='y', prejobs=[Job(name='1')]): ...,
                                },
                            ): ...,
                        },
                    ),
                ]),
            ],
            ['a', 'ɑ', '1', 'b', 'x', 'y', 'c', 'z', '10', '20', '2', 'β', '3'],
            id='Lots of mixed nested dependencies',
        ),
    ),
)
def test_get_job_and_dependencies(jobs, exp_job_names, make_TestTrackerJobs):
    tracker_jobs = make_TestTrackerJobs()
    required_jobs = tracker_jobs.get_job_and_dependencies(*jobs)
    assert [j.name for j in required_jobs] == exp_job_names


@pytest.mark.parametrize('isolated_jobs', ((), ('mock isolated job',)))
@pytest.mark.parametrize(
    argnames='jobs_before_upload, exp_submission_ok',
    argvalues=(
        ((), False),
        # All jobs exited successfully
        ((Mock(exit_code=0, is_enabled=True), Mock(exit_code=0, is_enabled=True), Mock(exit_code=0, is_enabled=True)), True),

        # Job exited with non-zero exit_code
        ((Mock(exit_code=0, is_enabled=True), Mock(exit_code=0, is_enabled=True), Mock(exit_code=1, is_enabled=True)), False),
        ((Mock(exit_code=0, is_enabled=True), Mock(exit_code=1, is_enabled=True), Mock(exit_code=0, is_enabled=True)), False),
        ((Mock(exit_code=1, is_enabled=True), Mock(exit_code=0, is_enabled=True), Mock(exit_code=0, is_enabled=True)), False),

        # Job is disabled
        ((Mock(exit_code=None, is_enabled=False), Mock(exit_code=0, is_enabled=True), Mock(exit_code=0, is_enabled=True)), True),
        ((Mock(exit_code=0, is_enabled=True), Mock(exit_code=None, is_enabled=False), Mock(exit_code=0, is_enabled=True)), True),
        ((Mock(exit_code=0, is_enabled=True), Mock(exit_code=0, is_enabled=False), Mock(exit_code=None, is_enabled=False)), True),
    ),
)
def test_submission_ok(isolated_jobs, jobs_before_upload, exp_submission_ok, make_TestTrackerJobs, mocker):
    tracker_jobs = make_TestTrackerJobs()
    mocker.patch.object(type(tracker_jobs), 'jobs_before_upload', PropertyMock(return_value=jobs_before_upload))
    mocker.patch.object(type(tracker_jobs), 'isolated_jobs', PropertyMock(return_value=isolated_jobs))
    if isolated_jobs:
        assert tracker_jobs.submission_ok is False
    else:
        assert tracker_jobs.submission_ok == exp_submission_ok


@pytest.mark.parametrize(
    argnames='job_name, tracker_name, exp_name',
    argvalues=(
        ('myjob', 'mytracker', 'myjob.mytracker'),
        ('myjob.mytracker', 'mytracker', 'myjob.mytracker'),
    ),
)
def test_get_job_name(job_name, tracker_name, exp_name, tracker, make_TestTrackerJobs, mocker):
    tracker.name = tracker_name
    tracker_jobs = make_TestTrackerJobs()
    assert tracker_jobs.get_job_name(job_name) == exp_name


def test_create_torrent_job(make_TestTrackerJobs, mocker):
    CreateTorrentJob_mock = mocker.patch('upsies.jobs.torrent.CreateTorrentJob')
    tracker_jobs = make_TestTrackerJobs(
        content_path='path/to/content',
        reuse_torrent_path='path/to/existing.torrent',
        tracker='mock tracker',
        exclude_files=('a', 'b', 'c'),
        common_job_args={'home_directory': 'path/to/home', 'ignore_cache': False},
    )
    mocker.patch.object(tracker_jobs, 'make_precondition')
    assert tracker_jobs.create_torrent_job is CreateTorrentJob_mock.return_value
    assert CreateTorrentJob_mock.call_args_list == [
        call(
            content_path='path/to/content',
            reuse_torrent_path='path/to/existing.torrent',
            tracker='mock tracker',
            exclude_files=('a', 'b', 'c'),
            precondition=tracker_jobs.make_precondition.return_value,
            home_directory='path/to/home',
            ignore_cache=False,
        ),
    ]
    assert tracker_jobs.make_precondition.call_args_list == [call('create_torrent_job')]

def test_create_torrent_job_is_singleton(make_TestTrackerJobs, mocker):
    mocker.patch('upsies.jobs.torrent.CreateTorrentJob', side_effect=(Mock(), Mock()))
    tracker_jobs = make_TestTrackerJobs()
    assert tracker_jobs.create_torrent_job is tracker_jobs.create_torrent_job


@pytest.mark.parametrize(
    argnames='btclient, create_torrent_job, exp_add_torrent_job_is_None',
    argvalues=(
        (Mock(), Mock(), False),
        (None, Mock(), True),
        (Mock(), None, True),
    ),
)
def test_add_torrent_job(btclient, create_torrent_job, exp_add_torrent_job_is_None, make_TestTrackerJobs, mocker):
    AddTorrentJob_mock = mocker.patch('upsies.jobs.torrent.AddTorrentJob')
    tracker_jobs = make_TestTrackerJobs(
        common_job_args={'home_directory': 'path/to/home', 'ignore_cache': False},
        btclient=btclient,
    )
    mocker.patch.object(type(tracker_jobs), 'create_torrent_job', PropertyMock(return_value=create_torrent_job))
    mocker.patch.object(tracker_jobs, 'make_precondition')
    if exp_add_torrent_job_is_None:
        assert tracker_jobs.add_torrent_job is None
        assert AddTorrentJob_mock.call_args_list == []
        assert tracker_jobs.make_precondition.call_args_list == []
    else:
        assert tracker_jobs.add_torrent_job is AddTorrentJob_mock.return_value
        assert AddTorrentJob_mock.call_args_list == [
            call(
                autostart=False,
                btclient=btclient,
                precondition=tracker_jobs.make_precondition.return_value,
                home_directory='path/to/home',
                ignore_cache=False,
            ),
        ]
        assert tracker_jobs.create_torrent_job.signal.register.call_args_list == [
            call('output', tracker_jobs.add_torrent_job.enqueue),
            call('finished', tracker_jobs.finalize_add_torrent_job),
        ]
        assert tracker_jobs.make_precondition.call_args_list == [call('add_torrent_job')]

def test_add_torrent_job_is_singleton(make_TestTrackerJobs, mocker):
    mocker.patch('upsies.jobs.torrent.AddTorrentJob', side_effect=(Mock(), Mock()))
    mocker.patch('upsies.jobs.torrent.CreateTorrentJob')
    tracker_jobs = make_TestTrackerJobs()
    assert tracker_jobs.add_torrent_job is tracker_jobs.add_torrent_job


def test_finalize_add_torrent_job(make_TestTrackerJobs, mocker):
    mocker.patch('upsies.jobs.torrent.AddTorrentJob')
    mocker.patch('upsies.jobs.torrent.CreateTorrentJob')
    tracker_jobs = make_TestTrackerJobs()
    mocker.patch.object(tracker_jobs, 'add_torrent_job')
    tracker_jobs.finalize_add_torrent_job('mock job')
    assert tracker_jobs.add_torrent_job.close.call_args_list == [call()]


@pytest.mark.parametrize(
    argnames='torrent_destination, create_torrent_job, exp_copy_torrent_job_is_None',
    argvalues=(
        ('some/path', Mock(), False),
        (None, Mock(), True),
        ('some/path', None, True),
    ),
)
def test_copy_torrent_job(
        torrent_destination, create_torrent_job, exp_copy_torrent_job_is_None,
        make_TestTrackerJobs, mocker,
):
    CopyTorrentJob_mock = mocker.patch('upsies.jobs.torrent.CopyTorrentJob')
    tracker_jobs = make_TestTrackerJobs(
        common_job_args={'home_directory': 'path/to/home', 'ignore_cache': False},
        torrent_destination=torrent_destination,
    )
    mocker.patch.object(type(tracker_jobs), 'create_torrent_job', PropertyMock(return_value=create_torrent_job))
    mocker.patch.object(tracker_jobs, 'make_precondition')
    if exp_copy_torrent_job_is_None:
        assert tracker_jobs.copy_torrent_job is None
        assert CopyTorrentJob_mock.call_args_list == []
        assert tracker_jobs.make_precondition.call_args_list == []
    else:
        assert tracker_jobs.copy_torrent_job is CopyTorrentJob_mock.return_value
        assert CopyTorrentJob_mock.call_args_list == [
            call(
                autostart=False,
                destination=torrent_destination,
                precondition=tracker_jobs.make_precondition.return_value,
                home_directory='path/to/home',
                ignore_cache=False,
            ),
        ]
        assert tracker_jobs.create_torrent_job.signal.register.call_args_list == [
            call('output', tracker_jobs.copy_torrent_job.enqueue),
            call('finished', tracker_jobs.finalize_copy_torrent_job),
        ]
        assert tracker_jobs.make_precondition.call_args_list == [call('copy_torrent_job')]

def test_copy_torrent_job_is_singleton(make_TestTrackerJobs, mocker):
    mocker.patch('upsies.jobs.torrent.CopyTorrentJob', side_effect=(Mock(), Mock()))
    mocker.patch('upsies.jobs.torrent.CreateTorrentJob')
    tracker_jobs = make_TestTrackerJobs()
    assert tracker_jobs.copy_torrent_job is tracker_jobs.copy_torrent_job


def test_finalize_copy_torrent_job(make_TestTrackerJobs, mocker):
    mocker.patch('upsies.jobs.torrent.CopyTorrentJob')
    mocker.patch('upsies.jobs.torrent.CreateTorrentJob')
    tracker_jobs = make_TestTrackerJobs()
    mocker.patch.object(tracker_jobs, 'copy_torrent_job')
    tracker_jobs.finalize_copy_torrent_job('mock job')
    assert tracker_jobs.copy_torrent_job.close.call_args_list == [call()]


def test_torrent_filepath(make_TestTrackerJobs, mocker):
    tracker_jobs = make_TestTrackerJobs()
    mocker.patch.object(type(tracker_jobs), 'create_torrent_job', PropertyMock(
        return_value='<mock create_torrent_job>',
    ))
    mocker.patch.object(tracker_jobs, 'get_job_output', return_value='path/to/file.torrent')

    assert tracker_jobs.torrent_filepath == 'path/to/file.torrent'
    assert tracker_jobs.get_job_output.call_args_list == [
        call(tracker_jobs.create_torrent_job, slice=0),
    ]


def test_subtitles(make_TestTrackerJobs, mocker):
    get_subtitles_mock = mocker.patch('upsies.utils.subtitle.get_subtitles')
    tracker_jobs = make_TestTrackerJobs()
    for _ in range(3):
        assert tracker_jobs.subtitles is get_subtitles_mock.return_value
    assert get_subtitles_mock.call_args_list == [
        call(tracker_jobs.content_path),
    ]


def test_release_name(make_TestTrackerJobs, mocker):
    ReleaseName_mock = mocker.patch('upsies.utils.release.ReleaseName')
    tracker_jobs = make_TestTrackerJobs(
        content_path='path/to/content',
    )
    assert tracker_jobs.release_name is ReleaseName_mock.return_value
    assert ReleaseName_mock.call_args_list == [
        call(
            path='path/to/content',
            translate=tracker_jobs.release_name_translation,
            separator=tracker_jobs.release_name_separator,
        ),
    ]


def test_release_name_job(make_TestTrackerJobs, mocker):
    TextFieldJob_mock = mocker.patch('upsies.jobs.dialog.TextFieldJob')
    tracker_jobs = make_TestTrackerJobs(
        content_path='path/to/content',
        common_job_args={'home_directory': 'path/to/home', 'ignore_cache': False},
    )

    mocker.patch.object(type(tracker_jobs), 'release_name', PropertyMock())
    mocker.patch.object(tracker_jobs, 'get_job_name')
    mocker.patch.object(tracker_jobs, 'make_precondition')

    release_name_job = tracker_jobs.release_name_job
    assert release_name_job is TextFieldJob_mock.return_value
    assert TextFieldJob_mock.call_args_list == [
        call(
            name=tracker_jobs.get_job_name.return_value,
            label='Release Name',
            callbacks={
                'output': tracker_jobs.release_name.set_release_info,
            },
            precondition=tracker_jobs.make_precondition.return_value,
            validator=tracker_jobs.validate_release_name,
            home_directory='path/to/home',
            ignore_cache=False,
        ),
    ]
    assert tracker_jobs.make_precondition.call_args_list == [call('release_name_job')]

def test_release_name_job_is_singleton(make_TestTrackerJobs, mocker):
    mocker.patch('upsies.jobs.dialog.TextFieldJob', side_effect=(Mock(), Mock()))
    tracker_jobs = make_TestTrackerJobs()
    mocker.patch.object(type(tracker_jobs), 'release_name', PropertyMock())
    assert tracker_jobs.release_name_job is tracker_jobs.release_name_job


@pytest.mark.parametrize(
    argnames='text, exp_exception',
    argvalues=(
        ('', ValueError('Release name must not be empty.')),
        (' ', ValueError('Release name must not be empty.')),
        ('Foo 2012 UNKNOWN_YEAR BluRay-ASDF', ValueError('Replace "UNKNOWN_YEAR" with the proper year.')),
        ('Foo 2012 BluRay UNKNOWN_AUDIO_FORMAT-ASDF', ValueError('Replace "UNKNOWN_AUDIO_FORMAT" with the proper audio format.')),
        ('Foo.2012.UNKNOWN_RESOLUTION.BluRay-ASDF', ValueError('Replace "UNKNOWN_RESOLUTION" with the proper resolution.')),
        ('Foo 2012 BluRay-ASDF', None),
    ),
    ids=lambda v: repr(v),
)
def test_validate_release_name(text, exp_exception, make_TestTrackerJobs):
    jobs = make_TestTrackerJobs()

    if exp_exception:
        with pytest.raises(type(exp_exception), match=rf'^{re.escape(str(exp_exception))}$'):
            jobs.validate_release_name(text)
    else:
        assert jobs.validate_release_name(text) is None


@pytest.mark.asyncio
async def test_update_release_name_from(make_TestTrackerJobs, mocker):
    tracker_jobs = make_TestTrackerJobs()
    mocker.patch.object(type(tracker_jobs), 'release_name', PropertyMock(return_value=Mock(
        fetch_info=Mock(),
    )))
    mocker.patch.object(type(tracker_jobs), 'release_name_job', PropertyMock(return_value=Mock(
        fetch_text=AsyncMock(),
    )))
    webdb = Mock()
    await tracker_jobs.update_release_name_from(webdb, 'tt123456')
    assert tracker_jobs.release_name_job.fetch_text.call_args_list == [
        call(
            coro=tracker_jobs.release_name.fetch_info.return_value,
            nonfatal_exceptions=(errors.RequestError,),
            default=str(tracker_jobs.release_name),
        ),
    ]
    assert tracker_jobs.release_name.fetch_info.call_args_list == [call(webdb=webdb, webdb_id='tt123456')]


def test_imdb_job(make_TestTrackerJobs, mocker):
    tracker_jobs = make_TestTrackerJobs(
        content_path='path/to/content',
        common_job_args={'home_directory': 'path/to/home', 'ignore_cache': False},
    )
    WebDbSearchJob_mock = mocker.patch('upsies.jobs.webdb.WebDbSearchJob')
    mocker.patch.object(tracker_jobs, 'make_precondition')
    imdb_job = tracker_jobs.imdb_job
    assert imdb_job is WebDbSearchJob_mock.return_value
    assert WebDbSearchJob_mock.call_args_list == [
        call(
            query='path/to/content',
            db=tracker_jobs.imdb,
            show_poster=tracker_jobs._show_poster,
            callbacks={
                'output': tracker_jobs._handle_imdb_id,
            },
            precondition=tracker_jobs.make_precondition.return_value,
            home_directory='path/to/home',
            ignore_cache=False,
        ),
    ]
    assert tracker_jobs.make_precondition.call_args_list == [call('imdb_job')]

def test_imdb_job_is_singleton(make_TestTrackerJobs, mocker):
    mocker.patch('upsies.jobs.webdb.WebDbSearchJob', side_effect=(Mock(), Mock()))
    tracker_jobs = make_TestTrackerJobs()
    assert tracker_jobs.imdb_job is tracker_jobs.imdb_job


def test_handle_imdb_id(make_TestTrackerJobs, mocker):
    tracker_jobs = make_TestTrackerJobs()
    imdb_id = 'tt123456'
    imdb = Mock()

    mocks = Mock()
    mocks.attach_mock(mocker.patch.object(tracker_jobs.tracker, 'attach_task'), 'attach_task')
    mocks.attach_mock(mocker.patch.object(tracker_jobs, '_propagate_webdb_info', Mock()), '_propagate_webdb_info')
    mocker.patch.object(type(tracker_jobs), 'imdb', PropertyMock(return_value=imdb))

    tracker_jobs._handle_imdb_id(imdb_id)
    assert mocks.mock_calls == [
        call._propagate_webdb_info(tracker_jobs.imdb, imdb_id),
        call.attach_task(tracker_jobs._propagate_webdb_info.return_value),
    ]


def test_imdb_id_property(make_TestTrackerJobs, mocker):
    tracker_jobs = make_TestTrackerJobs()
    mocker.patch.object(tracker_jobs, '_get_webdb_id_from_job')
    return_value = tracker_jobs.imdb_id
    assert return_value is tracker_jobs._get_webdb_id_from_job.return_value
    assert tracker_jobs._get_webdb_id_from_job.call_args_list == [call(tracker_jobs.imdb_job)]


def test_tmdb_job(make_TestTrackerJobs, mocker):
    WebDbSearchJob_mock = mocker.patch('upsies.jobs.webdb.WebDbSearchJob')
    webdb_mock = mocker.patch('upsies.utils.webdbs.webdb')
    tracker_jobs = make_TestTrackerJobs(
        content_path='path/to/content',
        common_job_args={'home_directory': 'path/to/home', 'ignore_cache': False},
    )
    mocker.patch.object(tracker_jobs, 'make_precondition')
    assert tracker_jobs.tmdb_job is WebDbSearchJob_mock.return_value
    assert WebDbSearchJob_mock.call_args_list == [
        call(
            query='path/to/content',
            db=webdb_mock.return_value,
            show_poster=tracker_jobs._show_poster,
            callbacks={
                'output': tracker_jobs._handle_tmdb_id,
            },
            precondition=tracker_jobs.make_precondition.return_value,
            home_directory='path/to/home',
            ignore_cache=False,
        ),
    ]
    assert webdb_mock.call_args_list == [call('tmdb')]
    assert tracker_jobs.make_precondition.call_args_list == [call('tmdb_job')]


def test_tmdb_job_is_singleton(make_TestTrackerJobs, mocker):
    mocker.patch('upsies.jobs.webdb.WebDbSearchJob', side_effect=(Mock(), Mock()))
    tracker_jobs = make_TestTrackerJobs()
    assert tracker_jobs.tmdb_job is tracker_jobs.tmdb_job


def test_handle_tmdb_id(make_TestTrackerJobs, mocker):
    tracker_jobs = make_TestTrackerJobs()
    tmdb_id = 'movie/123456'
    tmdb = Mock()

    mocks = Mock()
    mocks.attach_mock(mocker.patch.object(tracker_jobs.tracker, 'attach_task'), 'attach_task')
    mocks.attach_mock(mocker.patch.object(tracker_jobs, '_propagate_webdb_info', Mock()), '_propagate_webdb_info')
    mocker.patch.object(type(tracker_jobs), 'tmdb', PropertyMock(return_value=tmdb))

    tracker_jobs._handle_tmdb_id(tmdb_id)
    assert mocks.mock_calls == [
        # call._propagate_webdb_info(tracker_jobs.tmdb, tmdb_id),
        # call.attach_task(tracker_jobs._propagate_webdb_info.return_value),
    ]


def test_tmdb_id_property(make_TestTrackerJobs, mocker):
    tracker_jobs = make_TestTrackerJobs()
    mocker.patch.object(tracker_jobs, '_get_webdb_id_from_job')
    return_value = tracker_jobs.tmdb_id
    assert return_value is tracker_jobs._get_webdb_id_from_job.return_value
    assert tracker_jobs._get_webdb_id_from_job.call_args_list == [call(tracker_jobs.tmdb_job)]


def test_tvmaze_job(make_TestTrackerJobs, mocker):
    WebDbSearchJob_mock = mocker.patch('upsies.jobs.webdb.WebDbSearchJob')
    webdb_mock = mocker.patch('upsies.utils.webdbs.webdb')
    tracker_jobs = make_TestTrackerJobs(
        content_path='path/to/content',
        common_job_args={'home_directory': 'path/to/home', 'ignore_cache': False},
    )
    mocker.patch.object(tracker_jobs, 'make_precondition')
    assert tracker_jobs.tvmaze_job is WebDbSearchJob_mock.return_value
    assert WebDbSearchJob_mock.call_args_list == [
        call(
            query='path/to/content',
            db=webdb_mock.return_value,
            show_poster=tracker_jobs._show_poster,
            callbacks={
                'output': tracker_jobs._handle_tvmaze_id,
            },
            precondition=tracker_jobs.make_precondition.return_value,
            home_directory='path/to/home',
            ignore_cache=False,
        ),
    ]
    assert webdb_mock.call_args_list == [call('tvmaze')]
    assert tracker_jobs.make_precondition.call_args_list == [call('tvmaze_job')]

def test_tvmaze_job_is_singleton(make_TestTrackerJobs, mocker):
    mocker.patch('upsies.jobs.webdb.WebDbSearchJob', side_effect=(Mock(), Mock()))
    tracker_jobs = make_TestTrackerJobs()
    assert tracker_jobs.tvmaze_job is tracker_jobs.tvmaze_job


def test_handle_tvmaze_id(make_TestTrackerJobs, mocker):
    tracker_jobs = make_TestTrackerJobs()
    tvmaze_id = '123456'
    tvmaze = Mock()

    mocks = Mock()
    mocks.attach_mock(mocker.patch.object(tracker_jobs.tracker, 'attach_task'), 'attach_task')
    mocks.attach_mock(mocker.patch.object(tracker_jobs, '_propagate_webdb_info', Mock()), '_propagate_webdb_info')
    mocker.patch.object(type(tracker_jobs), 'tvmaze', PropertyMock(return_value=tvmaze))

    tracker_jobs._handle_tvmaze_id(tvmaze_id)
    assert mocks.mock_calls == [
        call._propagate_webdb_info(tracker_jobs.tvmaze, tvmaze_id),
        call.attach_task(tracker_jobs._propagate_webdb_info.return_value),
    ]


def test_tvmaze_id_property(make_TestTrackerJobs, mocker):
    tracker_jobs = make_TestTrackerJobs()
    mocker.patch.object(tracker_jobs, '_get_webdb_id_from_job')
    return_value = tracker_jobs.tvmaze_id
    assert return_value is tracker_jobs._get_webdb_id_from_job.return_value
    assert tracker_jobs._get_webdb_id_from_job.call_args_list == [call(tracker_jobs.tvmaze_job)]


@pytest.mark.parametrize(
    argnames='webdb_job, exp_return_value',
    argvalues=(
        (Mock(is_finished=False, output=[]), None),
        (Mock(is_finished=False, output=['mock id']), None),
        (Mock(is_finished=False, output=['mock id', 'another mock id']), None),
        (Mock(is_finished=True, output=[]), None),
        (Mock(is_finished=True, output=['mock id']), 'mock id'),
        (Mock(is_finished=True, output=['mock id', 'another mock id']), 'mock id'),
    ),
)
def test_get_webdb_id_from_job(webdb_job, exp_return_value, make_TestTrackerJobs, mocker):
    tracker_jobs = make_TestTrackerJobs()
    return_value = tracker_jobs._get_webdb_id_from_job(webdb_job)
    assert return_value == exp_return_value


@pytest.mark.parametrize('english_title', ('', 'English Title'))
@pytest.mark.parametrize('origin_job_is_finished', (False, True))
@pytest.mark.asyncio
async def test_propagate_webdb_info(origin_job_is_finished, english_title, make_TestTrackerJobs, mocker):
    tracker_jobs = make_TestTrackerJobs()

    mocks = Mock(
        update_release_name_from=AsyncMock(),
    )
    mocker.patch.object(tracker_jobs, 'update_release_name_from', mocks.update_release_name_from)
    mocker.patch('upsies.utils.webdbs.webdb_names', mocks.webdb_names)
    mocks.webdb_names.return_value = ('adb', 'bdb', 'cdb', 'ddb')

    mocker.patch('upsies.utils.webdbs.Query', mocks.Query)

    def make_db(name, type, title_english, title_original, year):
        return types.SimpleNamespace(
            name=name,
            type=AsyncMock(return_value=type),
            title_english=AsyncMock(return_value=title_english),
            title_original=AsyncMock(return_value=title_original),
            year=AsyncMock(return_value=year),
        )

    adb = make_db('adb', 'type from adb', english_title, 'original title from adb', 'year from adb')
    bdb = make_db('bdb', 'type from bdb', 'english title from bdb', 'original title from bdb', 'year from bdb')
    cdb = make_db('cdb', 'type from cdb', 'english title from cdb', 'original title from cdb', 'year from cdb')
    ddb = make_db('ddb', 'type from ddb', 'english title from ddb', 'original title from ddb', 'year from ddb')
    mocker.patch.object(type(tracker_jobs), 'adb', PropertyMock(return_value=adb), create=True)
    mocker.patch.object(type(tracker_jobs), 'bdb', PropertyMock(return_value=bdb), create=True)
    mocker.patch.object(type(tracker_jobs), 'cdb', PropertyMock(return_value=cdb), create=True)
    mocker.patch.object(type(tracker_jobs), 'ddb', PropertyMock(return_value=ddb), create=True)

    def make_db_job(name, is_enabled, is_finished, search):
        return types.SimpleNamespace(
            name=name,
            is_enabled=is_enabled,
            is_finished=is_finished,
            search=search,
            query=getattr(mocks, name[:name.index('-')]).query,
        )

    adb_job = make_db_job('adb-id', True, origin_job_is_finished, mocks.adb.search)
    bdb_job = make_db_job('bdb-id', False, True, mocks.bdb.search)
    cdb_job = make_db_job('cdb-id', True, False, mocks.cdb.search)
    ddb_job = make_db_job('ddb-id', True, True, mocks.ddb.search)
    mocker.patch.object(type(tracker_jobs), 'adb_job', PropertyMock(return_value=adb_job), create=True)
    mocker.patch.object(type(tracker_jobs), 'bdb_job', PropertyMock(return_value=bdb_job), create=True)
    mocker.patch.object(type(tracker_jobs), 'cdb_job', PropertyMock(return_value=cdb_job), create=True)
    mocker.patch.object(type(tracker_jobs), 'ddb_job', PropertyMock(return_value=ddb_job), create=True)

    await tracker_jobs._propagate_webdb_info(tracker_jobs.adb, '123456')

    exp_title = english_title or 'original title from adb'
    assert mocks.mock_calls == [
        call.webdb_names(),
        call.Query(type='type from adb', title=exp_title, year='year from adb'),
        call.cdb.query.update(mocks.Query.return_value),
        call.update_release_name_from(tracker_jobs.adb, '123456'),
    ]


def test_screenshots_job(make_TestTrackerJobs, mocker):
    ScreenshotsJob_mock = mocker.patch('upsies.jobs.screenshots.ScreenshotsJob')
    tracker_jobs = make_TestTrackerJobs(
        content_path='path/to/content',
        common_job_args={'home_directory': 'path/to/home', 'ignore_cache': False},
    )
    mocker.patch.object(tracker_jobs, 'make_precondition')
    mocker.patch.object(type(tracker_jobs), 'screenshots_count', PropertyMock())
    mocker.patch.object(type(tracker_jobs), 'screenshots_from_all_videos', PropertyMock())
    mocker.patch.object(type(tracker_jobs), 'create_torrent_job', PropertyMock())
    assert tracker_jobs.screenshots_job is ScreenshotsJob_mock.return_value
    assert ScreenshotsJob_mock.call_args_list == [
        call(
            content_path='path/to/content',
            exclude_files=tracker_jobs.exclude_files,
            count=tracker_jobs.screenshots_count,
            from_all_videos=tracker_jobs.screenshots_from_all_videos,
            optimize=tracker_jobs._screenshots_optimization,
            precondition=tracker_jobs.make_precondition.return_value,
            home_directory='path/to/home',
            ignore_cache=False,
        ),
    ]
    assert tracker_jobs.make_precondition.call_args_list == [call('screenshots_job')]

def test_screenshots_job_is_singleton(make_TestTrackerJobs, mocker):
    mocker.patch('upsies.jobs.screenshots.ScreenshotsJob', side_effect=(Mock(), Mock()))
    tracker_jobs = make_TestTrackerJobs()
    mocker.patch.object(type(tracker_jobs), 'create_torrent_job', PropertyMock())
    assert tracker_jobs.screenshots_job is tracker_jobs.screenshots_job


def test_screenshots_count(make_TestTrackerJobs, mocker):
    tracker_jobs = make_TestTrackerJobs(
        options={'screenshots': 123},
    )
    assert tracker_jobs.screenshots_count == 123


def test_screenshots_from_all_videos(make_TestTrackerJobs, mocker):
    tracker_jobs = make_TestTrackerJobs()
    assert tracker_jobs.screenshots_from_all_videos is False


def test_image_host_config():
    assert TrackerJobsBase.image_host_config == {}


@pytest.mark.parametrize(
    argnames='image_hosts, screenshots_job, exp_upload_screenshots_job_is_None',
    argvalues=(
        (Mock(), Mock(), False),
        (None, Mock(), True),
        (Mock(), None, True),
    ),
)
def test_upload_screenshots_job(
        image_hosts, screenshots_job, exp_upload_screenshots_job_is_None,
        make_TestTrackerJobs, mocker,
):
    ImageHostJob_mock = mocker.patch('upsies.jobs.imghost.ImageHostJob')
    mocker.patch('upsies.jobs.screenshots.ScreenshotsJob')
    tracker_jobs = make_TestTrackerJobs(
        image_hosts=image_hosts,
        content_path='path/to/content',
        common_job_args={'home_directory': 'path/to/home', 'ignore_cache': False},
    )
    mocker.patch.object(type(tracker_jobs), 'screenshots_job', PropertyMock(return_value=screenshots_job))
    mocker.patch.object(tracker_jobs, 'make_precondition')
    if exp_upload_screenshots_job_is_None:
        assert tracker_jobs.upload_screenshots_job is None
        assert ImageHostJob_mock.call_args_list == []
        assert tracker_jobs.make_precondition.call_args_list == []
    else:
        assert tracker_jobs.upload_screenshots_job is ImageHostJob_mock.return_value
        assert ImageHostJob_mock.call_args_list == [call(
            imghosts=image_hosts,
            precondition=tracker_jobs.make_precondition.return_value,
            home_directory='path/to/home',
            ignore_cache=False,
        )]
        # ScreenshotsJob also registers a callback for "timestamps"
        assert tracker_jobs.screenshots_job.signal.register.call_args_list == [
            call('screenshots_total', tracker_jobs.upload_screenshots_job.set_images_total),
            call('output', tracker_jobs.upload_screenshots_job.enqueue),
            call('finished', tracker_jobs.finalize_upload_screenshots_job),
        ]
        assert tracker_jobs.make_precondition.call_args_list == [call('upload_screenshots_job')]

def test_upload_screenshots_job_is_singleton(make_TestTrackerJobs, mocker):
    mocker.patch('upsies.jobs.imghost.ImageHostJob', side_effect=(Mock(), Mock()))
    mocker.patch('upsies.jobs.screenshots.ScreenshotsJob')
    tracker_jobs = make_TestTrackerJobs()
    assert tracker_jobs.upload_screenshots_job is tracker_jobs.upload_screenshots_job


def test_poster_job(make_TestTrackerJobs, mocker):
    PosterJob_mock = mocker.patch('upsies.jobs.poster.PosterJob')
    tracker_jobs = make_TestTrackerJobs(
        common_job_args={'home_directory': 'path/to/home', 'ignore_cache': False},
    )
    mocker.patch.object(tracker_jobs, 'make_poster_job_precondition')
    assert tracker_jobs.poster_job is PosterJob_mock.return_value
    assert PosterJob_mock.call_args_list == [
        call(
            precondition=tracker_jobs.make_poster_job_precondition.return_value,
            home_directory='path/to/home',
            ignore_cache=False,
            getter=tracker_jobs.get_poster,
            width=tracker_jobs.poster_max_width,
            height=tracker_jobs.poster_max_height,
            write_to=None,
            imghosts=tracker_jobs.image_hosts,
        ),
    ]
    assert tracker_jobs.make_poster_job_precondition.call_args_list == [call()]

def test_poster_job_is_singleton(make_TestTrackerJobs, mocker):
    mocker.patch('upsies.jobs.poster.PosterJob', side_effect=(Mock(), Mock()))
    tracker_jobs = make_TestTrackerJobs()
    assert tracker_jobs.poster_job is tracker_jobs.poster_job


def test_make_poster_job_precondition(make_TestTrackerJobs, mocker):
    tracker_jobs = make_TestTrackerJobs()
    mocker.patch.object(tracker_jobs, 'make_precondition')
    precondition = tracker_jobs.make_poster_job_precondition()
    assert precondition is tracker_jobs.make_precondition.return_value
    assert tracker_jobs.make_precondition.call_args_list == [call('poster_job')]


@pytest.mark.parametrize(
    argnames=(
        'get_poster_from_user, get_poster_from_tracker, get_poster_from_webdb,'
        'exp_return_value, exp_mock_calls'
    ),
    argvalues=(
        pytest.param(
            AsyncMock(return_value='http://poster_from_user.jpg'),
            AsyncMock(return_value='http://poster_from_tracker.jpg'),
            AsyncMock(return_value='http://poster_from_webdb.jpg'),
            'http://poster_from_user.jpg',
            [
                call.get_poster_from_user(),
            ],
            id='Poster from user',
        ),
        pytest.param(
            AsyncMock(return_value=None),
            AsyncMock(return_value='http://poster_from_tracker.jpg'),
            AsyncMock(return_value='http://poster_from_webdb.jpg'),
            'http://poster_from_tracker.jpg',
            [
                call.get_poster_from_user(),
                call.get_poster_from_tracker(),
            ],
            id='Poster from tracker',
        ),
        pytest.param(
            AsyncMock(return_value=None),
            AsyncMock(return_value=None),
            AsyncMock(return_value='http://poster_from_webdb.jpg'),
            'http://poster_from_webdb.jpg',
            [
                call.get_poster_from_user(),
                call.get_poster_from_tracker(),
                call.get_poster_from_webdb(),
            ],
            id='Poster from WebDB',
        ),
        pytest.param(
            AsyncMock(return_value=None),
            AsyncMock(return_value=None),
            AsyncMock(return_value=None),
            None,
            [
                call.get_poster_from_user(),
                call.get_poster_from_tracker(),
                call.get_poster_from_webdb(),
            ],
            id='No poster found',
        ),
    ),
)
@pytest.mark.asyncio
async def test_get_poster(
        get_poster_from_user, get_poster_from_tracker, get_poster_from_webdb,
        exp_return_value, exp_mock_calls,
        make_TestTrackerJobs, mocker,
):
    tracker_jobs = make_TestTrackerJobs()

    mocks = Mock()
    mocks.attach_mock(
        mocker.patch.object(tracker_jobs, 'get_poster_from_user', get_poster_from_user),
        'get_poster_from_user',
    )
    mocks.attach_mock(
        mocker.patch.object(tracker_jobs, 'get_poster_from_tracker', get_poster_from_tracker),
        'get_poster_from_tracker',
    )
    mocks.attach_mock(
        mocker.patch.object(tracker_jobs, 'get_poster_from_webdb', get_poster_from_webdb),
        'get_poster_from_webdb',
    )

    return_value = await tracker_jobs.get_poster()
    assert return_value == exp_return_value
    assert mocks.mock_calls == exp_mock_calls


@pytest.mark.parametrize(
    argnames='options, exp_return_value',
    argvalues=(
        pytest.param(
            {'poster': 'http://host.local/poster.jpg'},
            'http://host.local/poster.jpg',
            id='User provided poster',
        ),
        pytest.param(
            {},
            None,
            id='User provided no poster',
        ),
    ),
)
@pytest.mark.asyncio
async def test_get_poster_from_user(options, exp_return_value, make_TestTrackerJobs, mocker):
    tracker_jobs = make_TestTrackerJobs()
    mocker.patch.object(type(tracker_jobs), 'options', PropertyMock(return_value=options)),
    return_value = await tracker_jobs.get_poster_from_user()
    assert return_value == exp_return_value


@pytest.mark.asyncio
async def test_get_poster_from_tracker(make_TestTrackerJobs, mocker):
    tracker_jobs = make_TestTrackerJobs()
    return_value = await tracker_jobs.get_poster_from_tracker()
    assert return_value is None


@pytest.fixture
def mocks_for_get_poster_from_webdb(make_TestTrackerJobs, mocker):
    jobs = make_TestTrackerJobs()
    mocks = Mock()
    mocks.poster_webdb_job.wait = AsyncMock()
    mocks.poster_webdb.poster_url = AsyncMock()
    mocker.patch.object(type(jobs), 'poster_webdb_job', PropertyMock(return_value=mocks.poster_webdb_job))
    mocker.patch.object(type(jobs), 'poster_webdb', PropertyMock(return_value=mocks.poster_webdb))
    mocker.patch.object(type(jobs), 'release_name', PropertyMock(return_value=mocks.release_name))
    mocks.attach_mock(mocker.patch.object(jobs, 'get_job_output', return_value='mock output'), 'get_job_output')
    return jobs, mocks

@pytest.mark.asyncio
async def test_get_poster_from_webdb__no_poster_webdb_job(mocks_for_get_poster_from_webdb, mocker):
    tracker_jobs, mocks = mocks_for_get_poster_from_webdb
    mocker.patch.object(type(tracker_jobs), 'poster_webdb_job', PropertyMock(return_value=None))
    return_value = await tracker_jobs.get_poster_from_webdb()
    assert return_value is None
    assert mocks.mock_calls == []

@pytest.mark.asyncio
async def test_get_poster_from_webdb__no_poster_webdb_id(mocks_for_get_poster_from_webdb, mocker):
    tracker_jobs, mocks = mocks_for_get_poster_from_webdb
    mocks.get_job_output.return_value = None
    return_value = await tracker_jobs.get_poster_from_webdb()
    assert return_value is None
    assert mocks.mock_calls == [
        call.poster_webdb_job.wait(),
        call.get_job_output(tracker_jobs.poster_webdb_job, slice=0, default=None),
    ]

@pytest.mark.asyncio
async def test_get_poster_from_webdb__webdb_cannot_find_poster(mocks_for_get_poster_from_webdb):
    tracker_jobs, mocks = mocks_for_get_poster_from_webdb
    mocks.poster_webdb.poster_url.return_value = ''
    return_value = await tracker_jobs.get_poster_from_webdb()
    assert return_value is None
    assert mocks.mock_calls == [
        call.poster_webdb_job.wait(),
        call.get_job_output(tracker_jobs.poster_webdb_job, slice=0, default=None),
        call.poster_webdb.poster_url(
            tracker_jobs.get_job_output.return_value,
            season=tracker_jobs.release_name.only_season,
        ),
    ]

@pytest.mark.asyncio
async def test_get_poster_from_webdb__returns_poster(mocks_for_get_poster_from_webdb):
    tracker_jobs, mocks = mocks_for_get_poster_from_webdb
    mocks.poster_webdb.poster_url.return_value = 'http://webdb.local/poster.jpg'
    return_value = await tracker_jobs.get_poster_from_webdb()
    assert return_value == 'http://webdb.local/poster.jpg'
    assert mocks.mock_calls == [
        call.poster_webdb_job.wait(),
        call.get_job_output(tracker_jobs.poster_webdb_job, slice=0, default=None),
        call.poster_webdb.poster_url(
            tracker_jobs.get_job_output.return_value,
            season=tracker_jobs.release_name.only_season,
        ),
    ]

@pytest.mark.asyncio
async def test_get_poster_from_webdb__ignores_RequestError(mocks_for_get_poster_from_webdb):
    tracker_jobs, mocks = mocks_for_get_poster_from_webdb
    mocks.poster_webdb.poster_url.side_effect = errors.RequestError('site is down')
    return_value = await tracker_jobs.get_poster_from_webdb()
    assert return_value is None
    assert mocks.mock_calls == [
        call.poster_webdb_job.wait(),
        call.get_job_output(tracker_jobs.poster_webdb_job, slice=0, default=None),
        call.poster_webdb.poster_url(
            tracker_jobs.get_job_output.return_value,
            season=tracker_jobs.release_name.only_season,
        ),
    ]


def test_poster_webdb_job(make_TestTrackerJobs, mocker):
    tracker_jobs = make_TestTrackerJobs()
    mocker.patch.object(type(tracker_jobs), '_poster_webdb_and_job', PropertyMock(
        return_value=('poster_webdb', 'poster_webdb_job'),
    ))
    assert tracker_jobs.poster_webdb_job == 'poster_webdb_job'


def test_poster_webdb(make_TestTrackerJobs, mocker):
    tracker_jobs = make_TestTrackerJobs()
    mocker.patch.object(type(tracker_jobs), '_poster_webdb_and_job', PropertyMock(
        return_value=('poster_webdb', 'poster_webdb_job'),
    ))
    assert tracker_jobs.poster_webdb == 'poster_webdb'


@pytest.mark.parametrize(
    argnames='is_enabled, was_started, in_jobs_before_upload',
    argvalues=(
        (False, False, False),

        (False, False, True),
        (False, True, False),
        (True, False, False),

        (False, True, True),
        # (True, False, True),  # poster_job is enabled
        (True, True, False),

        (True, True, True),
    ),
)
def test__poster_webdb_and_job__when_poster_job_is_disabled(
        is_enabled, was_started, in_jobs_before_upload,
        make_TestTrackerJobs, mocker,
):
    tracker_jobs = make_TestTrackerJobs()

    mocker.patch.object(type(tracker_jobs), 'poster_job', PropertyMock(return_value=Mock(
        is_enabled=is_enabled,
        was_started=was_started,
    )))
    if in_jobs_before_upload:
        jobs_before_upload = ('foo', tracker_jobs.poster_job, 'bar')
    else:
        jobs_before_upload = ('foo', 'bar')
    mocker.patch.object(type(tracker_jobs), 'jobs_before_upload', PropertyMock(return_value=jobs_before_upload))

    assert tracker_jobs._poster_webdb_and_job == (None, None)

@pytest.mark.parametrize(
    argnames=(
        'tvmaze_is_enabled, tvmaze_in_jobs_before_upload, release_type, '
        'imdb_is_enabled, imdb_in_jobs_before_upload, '
        'tmdb_is_enabled, tmdb_in_jobs_before_upload, '
        'exp_result'
    ),
    argvalues=(
        pytest.param(
            True, True, utils.types.ReleaseType.season,  # TVmaze
            True, True,  # IMDb
            True, True,  # TMDb
            ('tvmaze', 'tvmaze_job'),
            id='tvmaze for season',
        ),
        pytest.param(
            True, True, utils.types.ReleaseType.episode,  # TVmaze
            True, True,  # IMDb
            True, True,  # TMDb
            ('tvmaze', 'tvmaze_job'),
            id='tvmaze for episode',
        ),
        pytest.param(
            True, True, utils.types.ReleaseType.movie,  # TVmaze
            True, True,  # IMDb
            True, True,  # TMDb
            ('imdb', 'imdb_job'),
            id='imdb for movie',
        ),
        pytest.param(
            True, False, utils.types.ReleaseType.series,  # TVmaze
            True, True,  # IMDb
            True, True,  # TMDb
            ('imdb', 'imdb_job'),
            id='imdb if tvmaze is not used',
        ),
        pytest.param(
            False, True, utils.types.ReleaseType.series,  # TVmaze
            True, True,  # IMDb
            True, True,  # TMDb
            ('imdb', 'imdb_job'),
            id='imdb if tvmaze is not enabled',
        ),
        pytest.param(
            False, False, utils.types.ReleaseType.movie,  # TVmaze
            True, False,  # IMDb
            True, True,  # TMDb
            ('tmdb', 'tmdb_job'),
            id='tmdb if imdb is not used',
        ),
        pytest.param(
            False, False, utils.types.ReleaseType.movie,  # TVmaze
            False, True,  # IMDb
            True, True,  # TMDb
            ('tmdb', 'tmdb_job'),
            id='tmdb if imdb is not enabled',
        ),
        pytest.param(
            True, False, utils.types.ReleaseType.movie,  # TVmaze
            True, False,  # IMDb
            True, False,  # TMDb
            (None, None),
            id='error if no webdb job is used',
        ),
        pytest.param(
            False, True, utils.types.ReleaseType.movie,  # TVmaze
            False, True,  # IMDb
            False, True,  # TMDb
            (None, None),
            id='error if no webdb job is enabled',
        ),
    ),
)
def test__poster_webdb_and_job_returns(
        tvmaze_is_enabled, tvmaze_in_jobs_before_upload, release_type,
        imdb_is_enabled, imdb_in_jobs_before_upload,
        tmdb_is_enabled, tmdb_in_jobs_before_upload,
        exp_result,
        make_TestTrackerJobs, mocker,
):
    tracker_jobs = make_TestTrackerJobs()

    mocker.patch.object(type(tracker_jobs), 'poster_job', PropertyMock(return_value=Mock(
        is_enabled=True,
        was_started=False,
    )))
    mocker.patch.object(type(tracker_jobs), 'imdb_job', PropertyMock(return_value=Mock(is_enabled=imdb_is_enabled)))
    mocker.patch.object(type(tracker_jobs), 'imdb', PropertyMock())
    mocker.patch.object(type(tracker_jobs), 'tmdb_job', PropertyMock(return_value=Mock(is_enabled=tmdb_is_enabled)))
    mocker.patch.object(type(tracker_jobs), 'tmdb', PropertyMock())
    mocker.patch.object(type(tracker_jobs), 'tvmaze_job', PropertyMock(return_value=Mock(is_enabled=tvmaze_is_enabled)))
    mocker.patch.object(type(tracker_jobs), 'tvmaze', PropertyMock())
    mocker.patch.object(type(tracker_jobs.release_name), 'type', PropertyMock(return_value=release_type))

    jobs_before_upload = ['foo', tracker_jobs.poster_job, 'bar']
    if imdb_in_jobs_before_upload:
        jobs_before_upload.insert(1, tracker_jobs.imdb_job)
    if tmdb_in_jobs_before_upload:
        jobs_before_upload.insert(1, tracker_jobs.tmdb_job)
    if tvmaze_in_jobs_before_upload:
        jobs_before_upload.insert(1, tracker_jobs.tvmaze_job)
    print(jobs_before_upload)
    mocker.patch.object(type(tracker_jobs), 'jobs_before_upload', PropertyMock(return_value=jobs_before_upload))

    assert tracker_jobs._poster_webdb_and_job == tuple(
        (
            getattr(tracker_jobs, name)
            if name else
            None
        )
        for name in exp_result
    )


def test_finalize_upload_screenshots_job(make_TestTrackerJobs, mocker):
    tracker_jobs = make_TestTrackerJobs()
    mocker.patch.object(type(tracker_jobs), 'upload_screenshots_job', PropertyMock())
    tracker_jobs.finalize_upload_screenshots_job('mock job')
    assert tracker_jobs.upload_screenshots_job.close.call_args_list == [call()]


def test_mediainfo_job(make_TestTrackerJobs, mocker):
    MediainfoJob_mock = mocker.patch('upsies.jobs.mediainfo.MediainfoJob')
    tracker_jobs = make_TestTrackerJobs(
        content_path='path/to/content',
        common_job_args={'home_directory': 'path/to/home', 'ignore_cache': False},
    )
    mocker.patch.object(type(tracker_jobs), 'mediainfo_from_all_videos', PropertyMock(
        return_value='maybe from_all_videos?',
    )),
    mocker.patch.object(type(tracker_jobs), 'exclude_files', PropertyMock(
        return_value='exclude these files!',
    )),
    mocker.patch.object(tracker_jobs, 'make_precondition')
    assert tracker_jobs.mediainfo_job is MediainfoJob_mock.return_value
    assert MediainfoJob_mock.call_args_list == [
        call(
            content_path='path/to/content',
            from_all_videos='maybe from_all_videos?',
            exclude_files='exclude these files!',
            precondition=tracker_jobs.make_precondition.return_value,
            home_directory='path/to/home',
            ignore_cache=False,
        ),
    ]
    assert tracker_jobs.make_precondition.call_args_list == [call('mediainfo_job')]

def test_mediainfo_job_is_singleton(make_TestTrackerJobs, mocker):
    mocker.patch('upsies.jobs.mediainfo.MediainfoJob', side_effect=(Mock(), Mock()))
    tracker_jobs = make_TestTrackerJobs()
    assert tracker_jobs.mediainfo_job is tracker_jobs.mediainfo_job


def test_mediainfos_and_screenshots(make_TestTrackerJobs, mocker):
    tracker_jobs = make_TestTrackerJobs()

    mocker.patch.object(type(tracker_jobs), 'mediainfo_job', PropertyMock(return_value=Mock(mediainfos_by_file={
        'path/to/foo.mkv': '<mediainfo for foo.mkv>',
        'path/to/bar/VIDEO_TS/VTS_01_0.IFO': '<mediainfo for bar/VTS_01_0.IFO>',
        'path/to/bar/VIDEO_TS/VTS_01_1.VOB': '<mediainfo for bar/VTS_01_1.VOB>',
    })))
    mocker.patch.object(type(tracker_jobs), 'screenshots_job', PropertyMock(return_value=Mock(screenshots_by_file={
        'path/to/foo.mkv': ('path/to/foo.1.png', 'path/to/foo.2.png'),
        'path/to/bar/VIDEO_TS/VTS_01_1.VOB': ('VTS_01_1.VOB.1.jpg',),
        'path/to/baz.mkv': ('path/to/baz.1.png', 'path/to/baz.2.png', 'path/to/baz.3.png'),
    })))
    mocker.patch.object(type(tracker_jobs), 'upload_screenshots_job', PropertyMock(return_value=Mock(urls_by_file={
        'path/to/foo.1.png': 'https://foo.1.png',
        'path/to/foo.2.png': 'https://foo.2.png',
        'VTS_01_1.VOB.1.jpg': 'https://VTS_01_1.VOB.1.jpg',
        'path/to/baz.1.png': 'https://baz.1.png',
        'path/to/baz.2.png': 'https://baz.2.png',
    })))

    assert tracker_jobs.mediainfos_and_screenshots == {
        'path/to/foo.mkv': {
            'mediainfo': '<mediainfo for foo.mkv>',
            'screenshot_urls': ['https://foo.1.png', 'https://foo.2.png'],
        },
        'path/to/bar/VIDEO_TS/VTS_01_0.IFO': {
            'mediainfo': '<mediainfo for bar/VTS_01_0.IFO>',
            'screenshot_urls': [],
        },
        'path/to/bar/VIDEO_TS/VTS_01_1.VOB': {
            'mediainfo': '<mediainfo for bar/VTS_01_1.VOB>',
            'screenshot_urls': ['https://VTS_01_1.VOB.1.jpg'],
        },
        'path/to/baz.mkv': {
            'mediainfo': '',
            'screenshot_urls': ['https://baz.1.png', 'https://baz.2.png'],
        },
    }


@pytest.mark.parametrize(
    argnames='options, common_job_args, exp_kwargs',
    argvalues=(
        ({}, {'ignore_cache': True}, {'ignore_cache': True, 'force': None}),
        ({}, {'ignore_cache': False}, {'ignore_cache': True, 'force': None}),
        ({'is_scene': None}, {'ignore_cache': True}, {'ignore_cache': True, 'force': None}),
        ({'is_scene': None}, {'ignore_cache': False}, {'ignore_cache': True, 'force': None}),
        ({'is_scene': True}, {'ignore_cache': True}, {'ignore_cache': True, 'force': True}),
        ({'is_scene': True}, {'ignore_cache': False}, {'ignore_cache': True, 'force': True}),
        ({'is_scene': False}, {'ignore_cache': True}, {'ignore_cache': True, 'force': False}),
        ({'is_scene': False}, {'ignore_cache': False}, {'ignore_cache': True, 'force': False}),
    ),
    ids=lambda v: repr(v),
)
def test_scene_check_job(options, common_job_args, exp_kwargs, make_TestTrackerJobs, mocker):
    SceneCheckJob_mock = mocker.patch('upsies.jobs.scene.SceneCheckJob')
    tracker_jobs = make_TestTrackerJobs(
        content_path='path/to/content',
        common_job_args=common_job_args,
    )
    mocker.patch.object(type(tracker_jobs), 'options', PropertyMock(return_value=options))
    mocker.patch.object(tracker_jobs, 'make_precondition')
    assert tracker_jobs.scene_check_job is SceneCheckJob_mock.return_value
    assert SceneCheckJob_mock.call_args_list == [call(
        content_path='path/to/content',
        precondition=tracker_jobs.make_precondition.return_value,
        **exp_kwargs,
    )]
    assert tracker_jobs.make_precondition.call_args_list == [call('scene_check_job')]

def test_scene_check_job_is_singleton(make_TestTrackerJobs, mocker):
    mocker.patch('upsies.jobs.scene.SceneCheckJob', side_effect=(Mock(), Mock()))
    tracker_jobs = make_TestTrackerJobs()
    assert tracker_jobs.scene_check_job is tracker_jobs.scene_check_job


@pytest.mark.parametrize(
    argnames='job_attr, jobs_before_upload, jobs_after_upload, isolated_jobs, custom_precondition, exp_return_value',
    argvalues=(
        ('foo_job', (), (), (), None, False),
        ('foo_job', (), (), (), Mock(return_value=True), False),
        ('foo_job', (), (), (), Mock(return_value=False), False),

        ('foo_job', ('foo_job', 'bar_job'), ('baz_job',), (), None, True),
        ('foo_job', ('foo_job', 'bar_job'), ('baz_job',), (), Mock(return_value=True), True),
        ('foo_job', ('foo_job', 'bar_job'), ('baz_job',), (), Mock(return_value=False), False),

        ('bar_job', ('foo_job', 'bar_job'), ('baz_job',), (), None, True),
        ('bar_job', ('foo_job', 'bar_job'), ('baz_job',), (), Mock(return_value=True), True),
        ('bar_job', ('foo_job', 'bar_job'), ('baz_job',), (), Mock(return_value=False), False),

        ('baz_job', ('foo_job', 'bar_job'), ('baz_job',), (), None, True),
        ('baz_job', ('foo_job', 'bar_job'), ('baz_job',), (), Mock(return_value=True), True),
        ('baz_job', ('foo_job', 'bar_job'), ('baz_job',), (), Mock(return_value=False), False),

        ('baz_job', ('foo_job',), ('bar_job',), (), None, False),
        ('baz_job', ('foo_job',), ('bar_job',), (), Mock(return_value=True), False),
        ('baz_job', ('foo_job',), ('bar_job',), (), Mock(return_value=False), False),

        ('bar_job', (), ('bar_job',), (), None, True),
        ('bar_job', (), ('bar_job',), (), Mock(return_value=True), True),
        ('bar_job', (), ('bar_job',), (), Mock(return_value=False), False),

        ('foo_job', ('foo_job', 'bar_job'), ('baz_job',), ('foo_job',), None, True),
        ('foo_job', ('foo_job', 'bar_job'), ('baz_job',), ('foo_job',), Mock(return_value=True), True),
        ('foo_job', ('foo_job', 'bar_job'), ('baz_job',), ('foo_job',), Mock(return_value=False), False),

        ('bar_job', ('foo_job', 'bar_job'), ('baz_job',), ('foo_job',), None, False),
        ('bar_job', ('foo_job', 'bar_job'), ('baz_job',), ('foo_job',), Mock(return_value=True), False),
        ('bar_job', ('foo_job', 'bar_job'), ('baz_job',), ('foo_job',), Mock(return_value=False), False),

        ('bar_job', ('foo_job', 'bar_job'), ('baz_job',), ('foo_job', 'bar_job'), None, True),
        ('bar_job', ('foo_job', 'bar_job'), ('baz_job',), ('foo_job', 'bar_job'), Mock(return_value=True), True),
        ('bar_job', ('foo_job', 'bar_job'), ('baz_job',), ('foo_job', 'bar_job'), Mock(return_value=False), False),

        ('baz_job', ('foo_job', 'bar_job'), ('baz_job',), ('foo_job', 'bar_job'), None, False),
        ('baz_job', ('foo_job', 'bar_job'), ('baz_job',), ('foo_job', 'bar_job'), Mock(return_value=True), False),
        ('baz_job', ('foo_job', 'bar_job'), ('baz_job',), ('foo_job', 'bar_job'), Mock(return_value=False), False),
    ),
    ids=lambda v: str(v),
)
def test_make_precondition(job_attr, jobs_before_upload, jobs_after_upload, isolated_jobs, custom_precondition,
                           exp_return_value,
                           make_TestTrackerJobs, mocker):
    tracker_jobs = make_TestTrackerJobs()
    for attr in ('foo_job', 'bar_job', 'baz_job'):
        mocker.patch.object(type(tracker_jobs), attr, PropertyMock(), create=True)
    mocker.patch.object(type(tracker_jobs), 'jobs_before_upload', PropertyMock(
        return_value=[getattr(tracker_jobs, attr) for attr in jobs_before_upload],
    ))
    mocker.patch.object(type(tracker_jobs), 'jobs_after_upload', PropertyMock(
        return_value=[getattr(tracker_jobs, attr) for attr in jobs_after_upload],
    ))
    mocker.patch.object(type(tracker_jobs), 'isolated_jobs', PropertyMock(
        return_value=[getattr(tracker_jobs, attr) for attr in isolated_jobs],
    ))
    precondition = tracker_jobs.make_precondition(job_attr, precondition=custom_precondition)
    return_value = precondition()
    assert return_value == exp_return_value


@pytest.mark.parametrize(
    argnames='job, slice, default, exp_result',
    argvalues=(
        (
            Mock(is_finished=True, output=('foo', 'bar', 'baz')),
            None,
            TrackerJobsBase._NO_DEFAULT,
            ('foo', 'bar', 'baz'),
        ),
        (
            Mock(is_finished=True, output=('foo', 'bar', 'baz')),
            0,
            'ignored default',
            'foo',
        ),
        (
            Mock(is_finished=True, output=('foo', 'bar', 'baz')),
            1,
            TrackerJobsBase._NO_DEFAULT,
            'bar',
        ),
        (
            Mock(is_finished=True, output=('foo', 'bar', 'baz')),
            2,
            'ignored default',
            'baz',
        ),
        (
            Mock(is_finished=True, output=('foo', 'bar', 'baz')),
            builtins.slice(1, 3),
            TrackerJobsBase._NO_DEFAULT,
            ('bar', 'baz'),
        ),

        # Job is not Finished
        (
            Mock(is_finished=False, output=('foo', 'bar', 'baz')),
            None,
            TrackerJobsBase._NO_DEFAULT,
            RuntimeError('Cannot get output from unfinished job: asdf'),
        ),
        (
            Mock(is_finished=False, output=('foo', 'bar', 'baz')),
            None,
            'my default',
            'my default',
        ),
        (
            Mock(is_finished=False, output=('foo', 'bar', 'baz')),
            None,
            None,
            None,
        ),

        # Slicing output fails with IndexError
        (
            Mock(is_finished=True, output=('foo', 'bar', 'baz')),
            10,
            TrackerJobsBase._NO_DEFAULT,
            RuntimeError("Job finished with insufficient output: asdf: ('foo', 'bar', 'baz')"),
        ),
        (
            Mock(is_finished=True, output=('foo', 'bar', 'baz')),
            10,
            'my default',
            'my default',
        ),
        (
            Mock(is_finished=True, output=('foo', 'bar', 'baz')),
            10,
            None,
            None,
        ),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.asyncio
async def test_get_job_output(job, slice, default, exp_result, make_TestTrackerJobs, mocker):
    job.configure_mock(name='asdf')
    tracker_jobs = make_TestTrackerJobs()
    if isinstance(exp_result, Exception):
        with pytest.raises(type(exp_result), match=rf'^{re.escape(str(exp_result))}$'):
            tracker_jobs.get_job_output(job, slice, default=default)
    else:
        output = tracker_jobs.get_job_output(job, slice, default=default)
        assert output == exp_result


@pytest.mark.parametrize(
    argnames='job, attribute, default, exp_result',
    argvalues=(
        (
            Mock(is_finished=True, foo='bar'),
            'foo',
            TrackerJobsBase._NO_DEFAULT,
            'bar',
        ),
        (
            Mock(is_finished=True, foo='bar'),
            'foo',
            'ignored default',
            'bar',
        ),
        (
            Mock(is_finished=False, foo='bar'),
            'foo',
            TrackerJobsBase._NO_DEFAULT,
            RuntimeError('Cannot get attribute from unfinished job: asdf'),
        ),
        (
            Mock(is_finished=False, foo='bar'),
            'foo',
            'my default',
            'my default',
        ),
        (
            Mock(is_finished=True, foo='bar', spec=()),
            'no_such_attribute',
            TrackerJobsBase._NO_DEFAULT,
            AttributeError('no_such_attribute'),
        ),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.asyncio
async def test_get_job_attribute(job, attribute, default, exp_result, make_TestTrackerJobs, mocker):
    job.configure_mock(name='asdf')
    tracker_jobs = make_TestTrackerJobs()
    if isinstance(exp_result, Exception):
        with pytest.raises(type(exp_result), match=rf'{re.escape(str(exp_result))}'):
            tracker_jobs.get_job_attribute(job, attribute, default=default)
    else:
        value = tracker_jobs.get_job_attribute(job, attribute, default=default)
        assert value == exp_result


@pytest.mark.parametrize(
    argnames='file_path, content_path, exp_result',
    argvalues=(
        (
            '/path/to/somewhere',
            '/this/is/completely/different',
            ValueError(r"'[\w+/]*to/somewhere' is not a subpath of '[\w+/]*completely'"),
        ),
        (
            '{tmp_path}/file.mkv',
            '{tmp_path}/file.mkv',
            'file.mkv',
        ),
        (
            '{tmp_path}/content/file_in_directory.mkv',
            '{tmp_path}/content',
            'content/file_in_directory.mkv',
        ),
        (
            '{tmp_path}/content/extras/file_in_subdirectory.mkv',
            '{tmp_path}/content',
            'content/extras/file_in_subdirectory.mkv',
        ),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.parametrize('file_path_is_relative', (False, True), ids=('file_path_is_absolute', 'file_path_is_relative'))
@pytest.mark.parametrize('content_path_is_relative', (False, True), ids=('content_path_is_absolute', 'content_path_is_relative'))
def test_get_relative_path(file_path, content_path, exp_result,
                           file_path_is_relative, content_path_is_relative,
                           tmp_path, make_TestTrackerJobs, mocker):

    def write(path):
        path = pathlib.Path(path.format(tmp_path=str(tmp_path)))
        try:
            path.relative_to(tmp_path)
        except ValueError:
            print(':::  not creating:', path)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            if path.suffix:
                print(':::  creating file:', path)
                path.write_bytes(b'content data')
            else:
                print(':::  creating directory:', path)
                path.mkdir(exist_ok=True)
        return path

    content_path = write(content_path)
    file_path = write(file_path)

    cwd = None
    orig_cwd = pathlib.Path(os.getcwd())
    if content_path_is_relative:
        cwd = content_path.parent.parent
        content_path = content_path.relative_to(cwd)
    if file_path_is_relative:
        if not cwd:
            cwd = file_path.parent.parent
        try:
            file_path = file_path.relative_to(cwd)
        except ValueError:
            pass

    print('___ content_path:', content_path)
    print('___ file_path:', file_path)
    print('___ cwd:', cwd)
    if cwd:
        if cwd.exists():
            os.chdir(cwd)
    try:
        tracker_jobs = make_TestTrackerJobs(
            content_path=str(content_path),
        )
        if isinstance(exp_result, Exception):
            exp_msg = type(exp_result)(str(exp_result).format(tmp_path=str(tmp_path)))
            with pytest.raises(type(exp_result), match=rf'^{exp_msg}$'):
                tracker_jobs.get_relative_file_path(str(file_path))
        else:
            relative_path = tracker_jobs.get_relative_file_path(str(file_path))
            assert relative_path == exp_result
    finally:
        if orig_cwd.exists():
            os.chdir(orig_cwd)


class ImageUrl(str):
    def __new__(cls, *args, thumbnail=True, **kwargs):
        self = super().__new__(cls, *args, **kwargs)
        self._thumbnail = thumbnail
        return self

    @property
    def thumbnail_url(self):
        if self._thumbnail:
            return f'thumb_{self}'

@pytest.mark.parametrize(
    argnames='screenshots, columns, horizontal_spacer, vertical_spacer, exp_bbcode',
    argvalues=(
        (
            (ImageUrl('a.png'), ImageUrl('b.png'), ImageUrl('c.png')),
            1, ' | ', '\n-\n',
            (
                '[url=a.png][img]thumb_a.png[/img][/url]'
                '\n-\n'
                '[url=b.png][img]thumb_b.png[/img][/url]'
                '\n-\n'
                '[url=c.png][img]thumb_c.png[/img][/url]'
            ),
        ),
        (
            (ImageUrl('a.png'), ImageUrl('b.png'), ImageUrl('c.png')),
            2, ' | ', '\n-\n',
            (
                '[url=a.png][img]thumb_a.png[/img][/url] | [url=b.png][img]thumb_b.png[/img][/url]'
                '\n-\n'
                '[url=c.png][img]thumb_c.png[/img][/url]'
            ),
        ),
        (
            (ImageUrl('a.png'), ImageUrl('b.png'), ImageUrl('c.png')),
            3, '|', '-',
            (
                '[url=a.png][img]thumb_a.png[/img][/url]|[url=b.png][img]thumb_b.png[/img][/url]|[url=c.png][img]thumb_c.png[/img][/url]'
            ),
        ),
        (
            (ImageUrl('a.png'), ImageUrl('b.png'), ImageUrl('c.png'), ImageUrl('d.png')),
            2, '.', ':',
            (
                '[url=a.png][img]thumb_a.png[/img][/url].[url=b.png][img]thumb_b.png[/img][/url]'
                ':'
                '[url=c.png][img]thumb_c.png[/img][/url].[url=d.png][img]thumb_d.png[/img][/url]'
            ),
        ),
        (
            (ImageUrl('a.png'), ImageUrl('b.png'), ImageUrl('c.png'), ImageUrl('d.png'), ImageUrl('e.png')),
            2, '.', ':',
            (
                '[url=a.png][img]thumb_a.png[/img][/url].[url=b.png][img]thumb_b.png[/img][/url]'
                ':'
                '[url=c.png][img]thumb_c.png[/img][/url].[url=d.png][img]thumb_d.png[/img][/url]'
                ':'
                '[url=e.png][img]thumb_e.png[/img][/url]'
            ),
        ),
        (
            (ImageUrl('a.png'), ImageUrl('b.png'), ImageUrl('c.png'), ImageUrl('d.png'), ImageUrl('e.png')),
            3, '.', ':',
            (
                '[url=a.png][img]thumb_a.png[/img][/url].[url=b.png][img]thumb_b.png[/img][/url].[url=c.png][img]thumb_c.png[/img][/url]'
                ':'
                '[url=d.png][img]thumb_d.png[/img][/url].[url=e.png][img]thumb_e.png[/img][/url]'
            ),
        ),
        (
            (ImageUrl('a.png'), ImageUrl('b.png'), ImageUrl('c.png'), ImageUrl('d.png'), ImageUrl('e.png'), ImageUrl('f.png')),
            2, '.', ':',
            (
                '[url=a.png][img]thumb_a.png[/img][/url].[url=b.png][img]thumb_b.png[/img][/url]'
                ':'
                '[url=c.png][img]thumb_c.png[/img][/url].[url=d.png][img]thumb_d.png[/img][/url]'
                ':'
                '[url=e.png][img]thumb_e.png[/img][/url].[url=f.png][img]thumb_f.png[/img][/url]'
            ),
        ),
        (
            (ImageUrl('a.png'), ImageUrl('b.png'), ImageUrl('c.png'), ImageUrl('d.png'), ImageUrl('e.png'), ImageUrl('f.png')),
            3, '.', ':',
            (
                '[url=a.png][img]thumb_a.png[/img][/url].[url=b.png][img]thumb_b.png[/img][/url].[url=c.png][img]thumb_c.png[/img][/url]'
                ':'
                '[url=d.png][img]thumb_d.png[/img][/url].[url=e.png][img]thumb_e.png[/img][/url].[url=f.png][img]thumb_f.png[/img][/url]'
            ),
        ),
    ),
)
def test_make_screenshots_grid(
        screenshots, columns, horizontal_spacer, vertical_spacer, exp_bbcode,
        make_TestTrackerJobs, mocker,
):
    tracker_jobs = make_TestTrackerJobs()
    bbcode = tracker_jobs.make_screenshots_grid(
        screenshots,
        columns=columns,
        horizontal_spacer=horizontal_spacer,
        vertical_spacer=vertical_spacer,
    )
    assert bbcode == exp_bbcode

def test_make_screenshots_grid_without_thumbnail_url(make_TestTrackerJobs, mocker):
    tracker_jobs = make_TestTrackerJobs()
    screenshots = (ImageUrl('a.png'), ImageUrl('b.png', thumbnail=False), ImageUrl('c.png'))
    with pytest.raises(RuntimeError, match=r'^No thumbnail for b\.png$'):
        tracker_jobs.make_screenshots_grid(screenshots)


@pytest.mark.parametrize(
    argnames='exception',
    argvalues=(
        errors.ContentError('Found unreadable nfo'),
        None,
    ),
    ids=lambda v: str(v),
)
def test_read_nfo(exception, make_TestTrackerJobs, mocker):
    tracker_jobs = make_TestTrackerJobs()
    mocker.patch.object(tracker_jobs, 'error')
    read_nfo_mock = mocker.patch('upsies.utils.string.read_nfo', side_effect=exception)
    strip = Mock()

    if exception:
        nfo = tracker_jobs.read_nfo(strip=strip)
        assert nfo is None
        assert tracker_jobs.error.call_args_list == [call(exception)]
    else:
        nfo = tracker_jobs.read_nfo(strip=strip)
        assert nfo is read_nfo_mock.return_value
        assert tracker_jobs.error.call_args_list == []

    assert read_nfo_mock.call_args_list == [call(tracker_jobs.content_path, strip=strip)]
