import os
from unittest.mock import AsyncMock, Mock, call

import pytest

from upsies import errors
from upsies.jobs.scene import SceneCheckJob
from upsies.utils.types import SceneCheckResult


@pytest.fixture
def make_SceneCheckJob(tmp_path):
    def make_SceneCheckJob(predb=None, force=None, content_path=tmp_path, ignore_cache=False):
        return SceneCheckJob(
            force=force,
            home_directory=tmp_path,
            cache_directory=tmp_path,
            ignore_cache=ignore_cache,
            content_path=content_path,
            predb=predb,
        )
    return make_SceneCheckJob


def test_cache_id(make_SceneCheckJob):
    job = make_SceneCheckJob()
    assert job.cache_id is None


@pytest.mark.parametrize('path', ('', 'path/to'))
@pytest.mark.parametrize(
    argnames='content_path, exp_content_stem',
    argvalues=(
        ('Foo', 'Foo'),
        ('//Foo///', 'Foo'),
        ('Foo.mkv', 'Foo'),
    ),
)
def test_content_stem(path, content_path, exp_content_stem, make_SceneCheckJob):
    job = make_SceneCheckJob(content_path=os.path.join(path, content_path))
    assert job.content_stem == exp_content_stem


def test_is_scene_release(make_SceneCheckJob):
    job = make_SceneCheckJob()
    job._is_scene_release = Mock()
    assert job.is_scene_release is job._is_scene_release
    job.signal.emit('checked', 'checked result')
    assert job.is_scene_release == 'checked result'


@pytest.mark.parametrize(
    argnames='is_scene_release',
    argvalues=(
        SceneCheckResult.true,
        SceneCheckResult.false,
        SceneCheckResult.unknown,
    ),
    ids=lambda v: str(v),
)
@pytest.mark.asyncio
async def test_is_scene_release_property_is_not_cached(is_scene_release, make_SceneCheckJob, mocker):
    mocker.patch('upsies.jobs.scene.SceneCheckJob._verify', AsyncMock())

    # Create the same job multiple times and expect uncached "is_scene_release"
    # each time until set_result() is called.
    for _ in range(3):
        job = make_SceneCheckJob(ignore_cache=False)
        job.start()
        assert job.is_scene_release is None
        job.set_result(is_scene_release)
        assert job.is_scene_release is is_scene_release
        await job.wait()


@pytest.mark.parametrize(
    argnames='kwargs, exp_attributes',
    argvalues=(
        ({}, {'_predetermined_result': None}),
        ({'force': None}, {'_predetermined_result': None}),
        ({'force': True}, {'_predetermined_result': True}),
        ({'force': 'false'}, {'_predetermined_result': True}),
        ({'force': False}, {'_predetermined_result': False}),
        ({'force': 0}, {'_predetermined_result': False}),
        ({'predb': 'mock predb'}, {'_predb': 'mock predb'}),
    ),
    ids=lambda v: str(v),
)
def test_initialize(kwargs, exp_attributes, make_SceneCheckJob, mocker):
    job = make_SceneCheckJob(**kwargs)
    for name, value in exp_attributes.items():
        assert getattr(job, name) == value


@pytest.mark.parametrize(
    argnames='exc, exp_exc, exp_cbs, exp_errors, exp_warnings',
    argvalues=(
        (
            None,
            None,
            [],
            (),
            (),
        ),
        (
            errors.SceneError('Foo'),
            None,
            [],
            (errors.SceneError('Foo'),),
            (),
        ),
        (
            errors.RequestError('Bar'),
            None,
            [call(SceneCheckResult.unknown)],
            (),
            ('Bar',),
        ),
    ),
    ids=lambda v: str(v),
)
@pytest.mark.asyncio
async def test_catch_errors(exc, exp_exc, exp_cbs, exp_errors, exp_warnings, make_SceneCheckJob, mocker):
    async def coro():
        if exc:
            raise exc

    ask_is_scene_release_cb = Mock()

    job = make_SceneCheckJob()
    job.signal.register('ask_is_scene_release', ask_is_scene_release_cb)

    await job._catch_errors(coro())

    assert job.errors == exp_errors
    assert job.warnings == exp_warnings

    assert ask_is_scene_release_cb.call_args_list == exp_cbs


@pytest.mark.parametrize(
    argnames='predetermined_result, exp_task_added, exp_result_set',
    argvalues=(
        (None, True, None),
        (True, False, SceneCheckResult.true),
        (False, False, SceneCheckResult.false),
    ),
)
@pytest.mark.asyncio
async def test_run(
        predetermined_result,
        exp_task_added, exp_result_set,
        make_SceneCheckJob, mocker,
):
    mocks = Mock()
    mocks.attach_mock(mocker.patch('upsies.jobs.scene.SceneCheckJob.add_task', Mock()), 'add_task')
    mocks.attach_mock(mocker.patch('upsies.jobs.scene.SceneCheckJob._catch_errors', Mock()), '_catch_errors')
    mocks.attach_mock(mocker.patch('upsies.jobs.scene.SceneCheckJob._verify', Mock()), '_verify')
    mocks.attach_mock(mocker.patch('upsies.jobs.scene.SceneCheckJob.set_result', Mock()), 'set_result')
    mocks.attach_mock(mocker.patch('upsies.jobs.scene.SceneCheckJob.finalization', AsyncMock()), 'finalization')
    job = make_SceneCheckJob(force=predetermined_result)

    await job.run()

    exp_mock_calls = []
    exp_check_tasks = []
    if exp_task_added:
        exp_mock_calls.append(call._verify())
        exp_mock_calls.append(call._catch_errors(job._verify.return_value))
        exp_mock_calls.append(call.add_task(job._catch_errors.return_value))
        exp_check_tasks = [job.add_task.return_value]

    elif exp_result_set is not None:
        exp_mock_calls.append(call.set_result(exp_result_set))

    exp_mock_calls.append(call.finalization())

    assert mocks.mock_calls == exp_mock_calls
    assert job._check_tasks == exp_check_tasks


@pytest.mark.parametrize(
    argnames='scene_check_result, exp_result_set',
    argvalues=(
        (SceneCheckResult.false, True),
        (SceneCheckResult.unknown, False),
        (SceneCheckResult.true, False),
    ),
)
@pytest.mark.asyncio
async def test_verify_sets_result_early_if_not_scene(scene_check_result, exp_result_set, make_SceneCheckJob, mocker):
    job = make_SceneCheckJob(
        content_path='path/to/foo',
        predb=Mock(
            search=AsyncMock(return_value=('first mock release', 'second mock release')),
            is_scene_release=AsyncMock(return_value=scene_check_result),
            verify_release=AsyncMock(),
        ),
    )
    is_mixed_season_pack_mock = mocker.patch('upsies.utils.predbs.is_mixed_season_pack', return_value=True)
    mocker.patch.object(job, '_verify_release', AsyncMock(
        return_value=('mock is_scene_release', 'mock exceptions'),
    ))
    mocker.patch.object(job, 'set_result')

    ask_release_name_cb = Mock()
    job.signal.register('ask_release_name', ask_release_name_cb)

    await job._verify()

    assert job._predb.is_scene_release.call_args_list == [call('path/to/foo')]
    if exp_result_set:
        assert job.set_result.call_args_list == [call(SceneCheckResult.false)]
        assert is_mixed_season_pack_mock.call_args_list == []
        assert ask_release_name_cb.call_args_list == []
        assert job._predb.search.call_args_list == []
        assert job._verify_release.call_args_list == []
    else:
        assert job.set_result.call_args_list == []
        assert is_mixed_season_pack_mock.call_args_list == [call('path/to/foo')]
        assert ask_release_name_cb.call_args_list == []
        assert job._predb.search.call_args_list == []
        assert job._verify_release.call_args_list == [call()]


@pytest.mark.asyncio
async def test_verify_verifies_release_if_it_is_mixed(make_SceneCheckJob, mocker):
    job = make_SceneCheckJob(
        content_path='path/to/foo',
        predb=Mock(
            search=AsyncMock(return_value=('first mock release', 'second mock release')),
            is_scene_release=AsyncMock(return_value=SceneCheckResult.true),
            verify_release=AsyncMock(),
        ),
    )
    is_mixed_season_pack_mock = mocker.patch('upsies.utils.predbs.is_mixed_season_pack', return_value=True)
    mocker.patch.object(job, '_verify_release', AsyncMock(
        return_value=('mock is_scene_release', 'mock exceptions'),
    ))
    mocker.patch.object(job, 'set_result', Mock())

    ask_release_name_cb = Mock()
    job.signal.register('ask_release_name', ask_release_name_cb)

    await job._verify()

    assert job._predb.is_scene_release.call_args_list == [call('path/to/foo')]
    assert job.set_result.call_args_list == []
    assert is_mixed_season_pack_mock.call_args_list == [call('path/to/foo')]
    assert ask_release_name_cb.call_args_list == []
    assert job._predb.search.call_args_list == []
    assert job._verify_release.call_args_list == [call()]


@pytest.mark.parametrize('extension', (None, 'mkv'))
@pytest.mark.parametrize(
    argnames='stem, search_results, exp_action',
    argvalues=(
        (
            'Foo.2003.720p.BluRay.x264-ASDF',
            ('Foo.2003.720p.BluRay.x264-ASDF', 'Foo.2003.720p.REPACK.BluRay.x264-ASDF'),
            'autoselect',
        ),
        (
            'Foo.2003.720p.REPACK.BluRay.x264-ASDF',
            ('Foo.2003.720p.BluRay.x264-ASDF', 'Foo.2003.720p.REPACK.BluRay.x264-ASDF'),
            'autoselect',
        ),
        (
            'Foo.2003.720p.BONUS.BluRay.x264-ASDF',
            ('Foo.2003.720p.BluRay.x264-ASDF', 'Foo.2003.720p.REPACK.BluRay.x264-ASDF'),
            'ask_user',
        ),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.asyncio
async def test_verify_autoselects_correctly_named_release_from_multiple_search_results(
        extension, stem, search_results, exp_action,
        make_SceneCheckJob, mocker,
):
    content_path = f'path/to/{stem}'
    if extension:
        content_path += f'.{extension}'

    job = make_SceneCheckJob(
        content_path=content_path,
        predb=Mock(
            search=AsyncMock(return_value=search_results),
            is_scene_release=AsyncMock(return_value=SceneCheckResult.true),
            verify_release=AsyncMock(),
        ),
    )
    is_mixed_season_pack_mock = mocker.patch('upsies.utils.predbs.is_mixed_season_pack', return_value=False)
    mocker.patch.object(job, '_verify_release', AsyncMock(
        return_value=('mock is_scene_release', 'mock exceptions')
    ))
    mocker.patch.object(job, 'set_result', Mock())

    ask_release_name_cb = Mock()
    job.signal.register('ask_release_name', ask_release_name_cb)

    await job._verify()

    assert job._predb.is_scene_release.call_args_list == [call(content_path)]
    assert job.set_result.call_args_list == []
    assert is_mixed_season_pack_mock.call_args_list == [call(content_path)]
    assert job._predb.search.call_args_list == [call(query=content_path, only_existing_releases=False)]
    if exp_action == 'autoselect':
        assert ask_release_name_cb.call_args_list == []
        assert job._verify_release.call_args_list == [call()]
    elif exp_action == 'ask_user':
        assert ask_release_name_cb.call_args_list == [call(search_results)]
        assert job._verify_release.call_args_list == []
    else:
        raise RuntimeError(f'Unexpected exp_action: {exp_action!r}')


@pytest.mark.asyncio
async def test_verify_verifies_release_if_there_is_one_search_result(make_SceneCheckJob, mocker):
    job = make_SceneCheckJob(
        content_path='path/to/foo',
        predb=Mock(
            search=AsyncMock(return_value=('single mock release',)),
            is_scene_release=AsyncMock(return_value=SceneCheckResult.true),
            verify_release=AsyncMock(),
        ),
    )
    is_mixed_season_pack_mock = mocker.patch('upsies.utils.predbs.is_mixed_season_pack', return_value=False)
    mocker.patch.object(job, '_verify_release', AsyncMock(
        return_value=('mock is_scene_release', 'mock exceptions')
    ))
    mocker.patch.object(job, 'set_result', Mock())

    ask_release_name_cb = Mock()
    job.signal.register('ask_release_name', ask_release_name_cb)

    await job._verify()

    assert job._predb.is_scene_release.call_args_list == [call('path/to/foo')]
    assert job.set_result.call_args_list == []
    assert is_mixed_season_pack_mock.call_args_list == [call('path/to/foo')]
    assert ask_release_name_cb.call_args_list == []
    assert job._predb.search.call_args_list == [call(query='path/to/foo', only_existing_releases=False)]
    assert job._verify_release.call_args_list == [call()]


@pytest.mark.asyncio
async def test_verify_asks_user_if_there_are_multiple_search_results(make_SceneCheckJob, mocker):
    job = make_SceneCheckJob(
        content_path='path/to/foo',
        predb=Mock(
            search=AsyncMock(return_value=('first mock release', 'second mock release')),
            is_scene_release=AsyncMock(return_value=SceneCheckResult.true),
            verify_release=AsyncMock(),
        ),
    )
    is_mixed_season_pack_mock = mocker.patch('upsies.utils.predbs.is_mixed_season_pack', return_value=False)
    mocker.patch.object(job, '_verify_release', AsyncMock(
        return_value=('mock is_scene_release', 'mock exceptions')
    ))
    mocker.patch.object(job, 'set_result', Mock())

    ask_release_name_cb = Mock()
    job.signal.register('ask_release_name', ask_release_name_cb)

    await job._verify()

    assert job._predb.is_scene_release.call_args_list == [call('path/to/foo')]
    assert job.set_result.call_args_list == []
    assert is_mixed_season_pack_mock.call_args_list == [call('path/to/foo')]
    assert ask_release_name_cb.call_args_list == [call(('first mock release', 'second mock release'))]
    assert job._predb.search.call_args_list == [call(query='path/to/foo', only_existing_releases=False)]
    assert job._verify_release.call_args_list == []


@pytest.mark.asyncio
async def test_user_selected_release_name_with_release_name(make_SceneCheckJob, mocker):
    job = make_SceneCheckJob()
    mocks = Mock()
    mocks.attach_mock(mocker.patch.object(job, 'add_task', Mock()), 'add_task')
    mocks.attach_mock(mocker.patch.object(job, '_catch_errors', Mock()), '_catch_errors')
    mocks.attach_mock(mocker.patch.object(job, '_verify_release', Mock()), '_verify_release')
    mocks.attach_mock(mocker.patch.object(job, '_handle_scene_check_result'), '_handle_scene_check_result')

    job.user_selected_release_name('mock.release.name')

    assert mocks.mock_calls == [
        call._verify_release('mock.release.name'),
        call._catch_errors(job._verify_release.return_value),
        call.add_task(job._catch_errors.return_value),
    ]

@pytest.mark.asyncio
async def test_user_selected_release_name_without_release_name(make_SceneCheckJob, mocker):
    job = make_SceneCheckJob()
    mocks = Mock()
    mocks.attach_mock(mocker.patch.object(job, 'add_task', Mock()), 'add_task')
    mocks.attach_mock(mocker.patch.object(job, '_catch_errors', Mock()), '_catch_errors')
    mocks.attach_mock(mocker.patch.object(job, '_verify_release', Mock()), '_verify_release')
    mocks.attach_mock(mocker.patch.object(job, '_handle_scene_check_result'), '_handle_scene_check_result')

    job.user_selected_release_name(None)

    assert mocks.mock_calls == [
        call._handle_scene_check_result(SceneCheckResult.false),
    ]


@pytest.mark.asyncio
async def test_verify_release(make_SceneCheckJob, mocker):
    job = make_SceneCheckJob(
        predb=Mock(
            verify_release=AsyncMock(
                return_value=(SceneCheckResult.true, ('error1', 'error2')),
            ),
        ),
    )
    mocker.patch.object(job, '_handle_scene_check_result')

    await job._verify_release('mock.release.name')

    assert job._predb.verify_release.call_args_list == [
        call(job._content_path, 'mock.release.name'),
    ]
    assert job._handle_scene_check_result.call_args_list == [
        call(SceneCheckResult.true, ('error1', 'error2')),
    ]


def test_handle_scene_check_result_handles_SceneErrors(make_SceneCheckJob, mocker):
    job = make_SceneCheckJob()

    mocks = Mock()
    mocks.attach_mock(mocker.patch.object(job, 'warn'), 'warn')
    mocks.attach_mock(mocker.patch.object(job, 'error'), 'error')
    mocks.attach_mock(mocker.patch.object(job, 'set_result'), 'set_result')
    job.signal.register('ask_is_scene_release', mocks.ask_is_scene_release_cb)

    job._handle_scene_check_result(
        'mock scene check result',
        exceptions=(
            errors.SceneError('foo'),
            errors.SceneRenamedError(original_name='bar', existing_name='Bar'),
            errors.SceneMissingInfoError('burr'),
            errors.SceneFileSizeError('baz', original_size=123, existing_size=456),
        ),
    )

    assert mocks.mock_calls == [
        call.warn(errors.SceneMissingInfoError('burr')),
        call.error(errors.SceneError('foo')),
        call.error(errors.SceneRenamedError(original_name='bar', existing_name='Bar')),
        call.error(errors.SceneFileSizeError('baz', original_size=123, existing_size=456)),
    ]


@pytest.mark.parametrize('is_scene_release', (SceneCheckResult.true, SceneCheckResult.false))
def test_handle_scene_check_result_handles_definite_scene_check_result(is_scene_release, make_SceneCheckJob, mocker):
    job = make_SceneCheckJob()

    mocks = Mock()
    mocks.attach_mock(mocker.patch.object(job, 'warn'), 'warn')
    mocks.attach_mock(mocker.patch.object(job, 'error'), 'error')
    mocks.attach_mock(mocker.patch.object(job, 'set_result'), 'set_result')
    job.signal.register('ask_is_scene_release', mocks.ask_is_scene_release_cb)

    job._handle_scene_check_result(is_scene_release, exceptions=())

    assert mocks.mock_calls == [
        call.set_result(is_scene_release),
    ]


@pytest.mark.parametrize('is_scene_release', (SceneCheckResult.unknown,))
def test_handle_scene_check_result_triggers_dialog_if_no_errors(is_scene_release, make_SceneCheckJob, mocker):
    job = make_SceneCheckJob()

    mocks = Mock()
    mocks.attach_mock(mocker.patch.object(job, 'warn'), 'warn')
    mocks.attach_mock(mocker.patch.object(job, 'error'), 'error')
    mocks.attach_mock(mocker.patch.object(job, 'set_result'), 'set_result')
    job.signal.register('ask_is_scene_release', mocks.ask_is_scene_release_cb)

    job._handle_scene_check_result(SceneCheckResult.unknown, ())

    assert mocks.mock_calls == [
        call.ask_is_scene_release_cb(SceneCheckResult.unknown),
    ]


@pytest.mark.parametrize(
    argnames='is_scene_release, exp_mock_calls',
    argvalues=(
        (
            SceneCheckResult.true,
            [
                call.emit('checked', SceneCheckResult.true),
                call.send('Scene release'),
                call.finalize(),
            ],
        ),
        (
            SceneCheckResult.false,
            [
                call.emit('checked', SceneCheckResult.false),
                call.send('Not a scene release'),
                call.finalize(),
            ],
        ),
        (
            SceneCheckResult.unknown,
            [
                call.emit('checked', SceneCheckResult.unknown),
                call.send('May be a scene release'),
                call.finalize(),
            ],
        ),
    ),
    ids=lambda v: str(v),
)
def test_set_result(is_scene_release, exp_mock_calls, make_SceneCheckJob, mocker):
    job = make_SceneCheckJob()
    mocks = Mock()
    mocks.attach_mock(mocker.patch.object(job.signal, 'emit'), 'emit')
    mocks.attach_mock(mocker.patch.object(job, 'send'), 'send')
    mocks.attach_mock(mocker.patch.object(job, 'finalize'), 'finalize')
    job.signal.register('checked', mocks.checked_cb)

    job.set_result(is_scene_release)

    assert mocks.mock_calls == exp_mock_calls


def test_stop_checking(make_SceneCheckJob, mocker):
    job = make_SceneCheckJob()
    job._check_tasks = [Mock(), Mock(), Mock()]

    job.stop_checking()

    for task in job._check_tasks:
        assert task.cancel.call_args_list == [call()]
