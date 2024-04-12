import io
import re
from unittest.mock import AsyncMock, Mock, call

import pytest

from upsies import errors
from upsies.trackers.bhd import BhdTracker, BhdTrackerConfig, BhdTrackerJobs
from upsies.utils.http import Response


def test_name_attribute():
    assert BhdTracker.name == 'bhd'


def test_label_attribute():
    assert BhdTracker.label == 'BHD'


def test_torrent_source_field_attribute():
    assert BhdTracker.torrent_source_field == 'BHD'


def test_TrackerConfig_attribute():
    assert BhdTracker.TrackerConfig is BhdTrackerConfig


def test_TrackerJobs_attribute():
    assert BhdTracker.TrackerJobs is BhdTrackerJobs


@pytest.mark.asyncio
async def test_login(mocker):
    tracker = BhdTracker()
    await tracker._login()


@pytest.mark.asyncio
async def test_logout(mocker):
    tracker = BhdTracker()
    await tracker._logout()


@pytest.mark.parametrize(
    argnames='announce_url',
    argvalues=(
        'http://bhd.tracker.local:1234/announce',
        'http://bhd.tracker.local:1234/announce/',
    ),
)
@pytest.mark.asyncio
async def test_get_announce_url(announce_url):
    tracker = BhdTracker(options={
        'announce_url': announce_url,
        'announce_passkey': 'd34db33f',
    })
    url = await tracker.get_announce_url()
    assert url == announce_url.rstrip('/') + '/d34db33f'


@pytest.mark.parametrize(
    argnames='upload_url',
    argvalues=(
        'http://bhd/upload',
        'http://bhd/upload/',
    ),
)
def test_get_upload_url(upload_url):
    tracker = BhdTracker(options={
        'upload_url': upload_url,
        'apikey': 'd34db33f',
    })
    url = tracker.get_upload_url()
    assert url == upload_url.rstrip('/') + '/d34db33f'

def test_get_upload_url_without_apikey():
    tracker = BhdTracker(options={
        'upload_url': 'http://localhost/upload',
        'apikey': '',
    })
    with pytest.raises(errors.RequestError, match=rf'^trackers.{tracker.name}.apikey is not set$'):
        tracker.get_upload_url()


@pytest.mark.asyncio
async def test_upload_gets_invalid_json(mocker):
    tracker = BhdTracker(options={'upload_url': 'http://bhd.local/upload', 'apikey': '1337'})
    tracker_jobs_mock = Mock(
        post_data={'foo': 'bar'},
        torrent_filepath='path/to/content.torrent',
        mediainfo_filehandle=io.StringIO('mediainfo mock'),
    )
    http_mock = mocker.patch('upsies.utils.http', Mock(
        post=AsyncMock(return_value=Response(
            text='{choke on this',
            bytes=b'irrelevant',
        )),
    ))
    with pytest.raises(errors.RequestError, match=r"^Malformed JSON: '\{choke on this"):
        await tracker.upload(tracker_jobs_mock)
    assert http_mock.post.call_args_list == [call(
        url='http://bhd.local/upload/1337',
        cache=False,
        user_agent=True,
        data=tracker_jobs_mock.post_data,
        files={
            'file': {
                'file': tracker_jobs_mock.torrent_filepath,
                'mimetype': 'application/octet-stream',
            },
            'mediainfo': {
                'file': tracker_jobs_mock.mediainfo_filehandle,
                'filename': 'mediainfo',
                'mimetype': 'application/octet-stream',
            },
        },
    )]

@pytest.mark.asyncio
async def test_upload_gets_error_status_code(mocker):
    tracker = BhdTracker(options={'upload_url': 'http://bhd.local/upload', 'apikey': '1337'})
    tracker_jobs_mock = Mock(
        post_data={'foo': 'bar'},
        torrent_filepath='path/to/content.torrent',
        mediainfo_filehandle=io.StringIO('mediainfo mock'),
    )
    http_mock = mocker.patch('upsies.utils.http', Mock(
        post=AsyncMock(return_value=Response(
            text='''
            {
                "status_code": 0,
                "success": false,
                "status_message": "This is the error message"
            }
            ''',
            bytes=b'irrelevant',
        )),
    ))
    with pytest.raises(errors.RequestError, match=r'^Upload failed: This is the error message$'):
        await tracker.upload(tracker_jobs_mock)
    assert http_mock.post.call_args_list == [call(
        url='http://bhd.local/upload/1337',
        cache=False,
        user_agent=True,
        data=tracker_jobs_mock.post_data,
        files={
            'file': {
                'file': tracker_jobs_mock.torrent_filepath,
                'mimetype': 'application/octet-stream',
            },
            'mediainfo': {
                'file': tracker_jobs_mock.mediainfo_filehandle,
                'filename': 'mediainfo',
                'mimetype': 'application/octet-stream',
            },
        },
    )]

@pytest.mark.asyncio
async def test_upload_gets_unexpected_status_code(mocker):
    tracker = BhdTracker(options={'upload_url': 'http://bhd.local/upload', 'apikey': '1337'})
    tracker_jobs_mock = Mock(
        post_data={'foo': 'bar'},
        torrent_filepath='path/to/content.torrent',
        mediainfo_filehandle=io.StringIO('mediainfo mock'),
    )
    http_mock = mocker.patch('upsies.utils.http', Mock(
        post=AsyncMock(return_value=Response(
            text='{"status_code": 123.5}',
            bytes=b'irrelevant',
        )),
    ))
    with pytest.raises(RuntimeError, match=r"^Unexpected response: '\{\"status_code\": 123.5\}'$"):
        await tracker.upload(tracker_jobs_mock)
    assert http_mock.post.call_args_list == [call(
        url='http://bhd.local/upload/1337',
        cache=False,
        user_agent=True,
        data=tracker_jobs_mock.post_data,
        files={
            'file': {
                'file': tracker_jobs_mock.torrent_filepath,
                'mimetype': 'application/octet-stream',
            },
            'mediainfo': {
                'file': tracker_jobs_mock.mediainfo_filehandle,
                'filename': 'mediainfo',
                'mimetype': 'application/octet-stream',
            },
        },
    )]

@pytest.mark.asyncio
async def test_upload_gets_unexpected_json(mocker):
    tracker = BhdTracker(options={'upload_url': 'http://bhd.local/upload', 'apikey': '1337'})
    tracker_jobs_mock = Mock(
        post_data={'foo': 'bar'},
        torrent_filepath='path/to/content.torrent',
        mediainfo_filehandle=io.StringIO('mediainfo mock'),
    )
    http_mock = mocker.patch('upsies.utils.http', Mock(
        post=AsyncMock(return_value=Response(
            text='{"hey": "you"}',
            bytes=b'irrelevant',
        )),
    ))
    with pytest.raises(RuntimeError, match=r"^Unexpected response: '\{\"hey\": \"you\"\}'$"):
        await tracker.upload(tracker_jobs_mock)
    assert http_mock.post.call_args_list == [call(
        url='http://bhd.local/upload/1337',
        cache=False,
        user_agent=True,
        data=tracker_jobs_mock.post_data,
        files={
            'file': {
                'file': tracker_jobs_mock.torrent_filepath,
                'mimetype': 'application/octet-stream',
            },
            'mediainfo': {
                'file': tracker_jobs_mock.mediainfo_filehandle,
                'filename': 'mediainfo',
                'mimetype': 'application/octet-stream',
            },
        },
    )]

@pytest.mark.asyncio
async def test_upload_succeeds(mocker):
    tracker = BhdTracker(options={'upload_url': 'http://bhd.local/upload', 'apikey': '1337'})
    tracker_jobs_mock = Mock(
        post_data={
            'foo': 'asdf',
            'bar': '',
            'baz': 0,
            'quux': '0',
            'quuz': None,
        },
        torrent_filepath='path/to/content.torrent',
        mediainfo_filehandle=io.StringIO('mediainfo mock'),
    )
    http_mock = mocker.patch('upsies.utils.http', Mock(
        post=AsyncMock(return_value=Response(
            text='''
            {
                "status_code": 2,
                "success": true,
                "status_message": "http://bhd.local/torrent/download/release_name.123456.d34db33f"
            }
            ''',
            bytes=b'irrelevant',
        )),
    ))
    torrent_page_url = await tracker.upload(tracker_jobs_mock)
    assert torrent_page_url == 'http://bhd.local/torrents/release_name.123456'
    assert http_mock.post.call_args_list == [call(
        url='http://bhd.local/upload/1337',
        cache=False,
        user_agent=True,
        data={
            'foo': 'asdf',
            'baz': '0',
            'quux': '0',
        },
        files={
            'file': {
                'file': tracker_jobs_mock.torrent_filepath,
                'mimetype': 'application/octet-stream',
            },
            'mediainfo': {
                'file': tracker_jobs_mock.mediainfo_filehandle,
                'filename': 'mediainfo',
                'mimetype': 'application/octet-stream',
            },
        },
    )]

@pytest.mark.asyncio
async def test_upload_draft_succeeds(mocker):
    tracker = BhdTracker(options={'upload_url': 'http://bhd.local/upload', 'apikey': '1337'})
    warning_cb = Mock()
    tracker.signal.register('warning', warning_cb)
    tracker_jobs_mock = Mock(
        post_data={'foo': 'bar'},
        torrent_filepath='path/to/content.torrent',
        mediainfo_filehandle=io.StringIO('mediainfo mock'),
    )
    http_mock = mocker.patch('upsies.utils.http', Mock(
        post=AsyncMock(return_value=Response(
            text='''
            {
                "status_code": 1,
                "success": true,
                "status_message": "Draft uploaded"
            }
            ''',
            bytes=b'irrelevant',
        )),
    ))
    torrent_filepath = await tracker.upload(tracker_jobs_mock)
    assert warning_cb.call_args_list == [
        call('Draft uploaded'),
        call('You have to activate your upload manually '
             'on the website when you are ready to seed.')
    ]
    assert torrent_filepath == tracker_jobs_mock.torrent_filepath
    assert http_mock.post.call_args_list == [call(
        url='http://bhd.local/upload/1337',
        cache=False,
        user_agent=True,
        data=tracker_jobs_mock.post_data,
        files={
            'file': {
                'file': tracker_jobs_mock.torrent_filepath,
                'mimetype': 'application/octet-stream',
            },
            'mediainfo': {
                'file': tracker_jobs_mock.mediainfo_filehandle,
                'filename': 'mediainfo',
                'mimetype': 'application/octet-stream',
            },
        },
    )]


@pytest.mark.parametrize(
    argnames='bytes, exp_piece_size',
    argvalues=(
        (-1, RuntimeError('Cannot calculate piece size for -1 bytes')),
        (0, RuntimeError('Cannot calculate piece size for 0 bytes')),
        # 1 MiB
        (1, 1 * (1024 ** 2)),
        (8 * (1024 ** 3) - 1, 1 * (1024 ** 2)),
        # 2 MiB
        (8 * (1024 ** 3), 2 * (1024 ** 2)),
        (16 * (1024 ** 3) - 1, 2 * (1024 ** 2)),
        # 4 MiB
        (16 * (1024 ** 3), 4 * (1024 ** 2)),
        (72 * (1024 ** 3) - 1, 4 * (1024 ** 2)),
        # 8 MiB
        (72 * (1024 ** 3), 8 * (1024 ** 2)),
        (float('inf'), 8 * (1024 ** 2)),
    ),
)
def test_calculate_piece_size(bytes, exp_piece_size):
    if isinstance(exp_piece_size, Exception):
        with pytest.raises(type(exp_piece_size), match=rf'^{re.escape(str(exp_piece_size))}$'):
            BhdTracker.calculate_piece_size(bytes)
    else:
        piece_size = BhdTracker.calculate_piece_size(bytes)
        assert piece_size == exp_piece_size
