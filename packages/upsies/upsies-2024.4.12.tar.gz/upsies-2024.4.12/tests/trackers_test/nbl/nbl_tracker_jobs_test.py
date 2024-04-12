from unittest.mock import Mock, PropertyMock, call

import pytest

from upsies import utils
from upsies.trackers import nbl


@pytest.fixture
def tracker():
    tracker = Mock()
    tracker.name = 'nbl'
    return tracker


@pytest.fixture
def nbl_tracker_jobs(tracker, tmp_path, mocker):
    content_path = tmp_path / 'Foo S01 1080p BluRay x264-ASDF'

    nbl_tracker_jobs = nbl.NblTrackerJobs(
        content_path=str(content_path),
        tracker=tracker,
        torrent_destination=str(tmp_path / 'destination'),
        common_job_args={
            'home_directory': str(tmp_path / 'home_directory'),
            'ignore_cache': True,
        },
        options=None,
    )

    return nbl_tracker_jobs


def test_jobs_before_upload(nbl_tracker_jobs, tmp_path, mocker):
    create_torrent_job_mock = mocker.patch('upsies.trackers.nbl.NblTrackerJobs.create_torrent_job', Mock())
    mediainfo_job_mock = mocker.patch('upsies.trackers.nbl.NblTrackerJobs.mediainfo_job', Mock())
    tvmaze_job_mock = mocker.patch('upsies.trackers.nbl.NblTrackerJobs.tvmaze_job', Mock())
    category_job_mock = mocker.patch('upsies.trackers.nbl.NblTrackerJobs.category_job', Mock())
    assert nbl_tracker_jobs.jobs_before_upload == (
        tvmaze_job_mock,
        category_job_mock,
        create_torrent_job_mock,
        mediainfo_job_mock,
    )


def test_category_job(nbl_tracker_jobs, mocker):
    ChoiceJob_mock = mocker.patch('upsies.jobs.dialog.ChoiceJob')
    mocker.patch.object(nbl_tracker_jobs, 'get_job_name')
    mocker.patch.object(nbl_tracker_jobs, 'make_precondition')
    mocker.patch.object(type(nbl_tracker_jobs), 'autodetected_category', PropertyMock(return_value='my category'))
    mocker.patch.object(nbl_tracker_jobs, 'common_job_args', return_value={'foo': 'bar'})

    assert nbl_tracker_jobs.category_job is ChoiceJob_mock.return_value
    assert ChoiceJob_mock.call_args_list == [call(
        name=nbl_tracker_jobs.get_job_name.return_value,
        label='Category',
        precondition=nbl_tracker_jobs.make_precondition.return_value,
        options=(
            ('Season', '3'),
            ('Episode', '1'),
        ),
        autodetected=nbl_tracker_jobs.autodetected_category,
        foo='bar',
    )]
    assert nbl_tracker_jobs.get_job_name.call_args_list == [call('category')]
    assert nbl_tracker_jobs.make_precondition.call_args_list == [call('category_job')]
    assert nbl_tracker_jobs.common_job_args.call_args_list == [call()]


@pytest.mark.parametrize(
    argnames='release_type, exp_category',
    argvalues=(
        (utils.release.ReleaseType.season, 'Season'),
        (utils.release.ReleaseType.episode, 'Episode'),
        (utils.release.ReleaseType.movie, 'Episode'),
    ),
    ids=lambda v: repr(v),
)
def test_autodetected_category(release_type, exp_category, nbl_tracker_jobs, mocker):
    mocker.patch.object(type(nbl_tracker_jobs.release_name), 'type', PropertyMock(return_value=release_type))
    return_value = nbl_tracker_jobs.autodetected_category
    assert return_value == exp_category


def test_post_data(nbl_tracker_jobs, mocker):
    mocker.patch.object(type(nbl_tracker_jobs), 'options', PropertyMock(return_value={
        'apikey': 'mock api key',
    }))
    mocker.patch.object(nbl_tracker_jobs, 'get_job_attribute', side_effect=(
        'mock category',
    ))
    mocker.patch.object(nbl_tracker_jobs, 'get_job_output', side_effect=(
        'mock tvmaze id',
        'mock mediainfo',
    ))
    mocker.patch.object(type(nbl_tracker_jobs), 'category_job', PropertyMock())
    mocker.patch.object(type(nbl_tracker_jobs), 'tvmaze_job', PropertyMock())
    mocker.patch.object(type(nbl_tracker_jobs), 'mediainfo_job', PropertyMock())

    assert nbl_tracker_jobs.post_data == {
        'api_key': 'mock api key',
        'category': 'mock category',
        'tvmazeid': 'mock tvmaze id',
        'mediainfo': 'mock mediainfo',
    }
    assert nbl_tracker_jobs.get_job_attribute.call_args_list == [
        call(nbl_tracker_jobs.category_job, 'choice'),
    ]
    assert nbl_tracker_jobs.get_job_output.call_args_list == [
        call(nbl_tracker_jobs.tvmaze_job, slice=0),
        call(nbl_tracker_jobs.mediainfo_job, slice=0),
    ]
