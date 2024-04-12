"""
Concrete :class:`~.base.TrackerConfigBase` subclass for PTP
"""

import base64
import re

from ...utils import argtypes, configfiles, is_running_in_development_environment, types
from ..base import TrackerConfigBase, exclude
from . import metadata

PtpImageHost = types.ImageHost(
    disallowed=(
        ()
        if is_running_in_development_environment() else
        ('dummy',)
    ),
)


class PtpReleaseType(str):
    def __new__(cls, text):
        for type, regex in metadata.types.items():
            if regex.search(text):
                return super().__new__(cls, type)
        raise argtypes.ArgumentTypeError(f'Invalid type: {text}')


class PtpImdbId(str):
    def __new__(cls, id):
        match = re.search(r'^(?:tt|)(\d+)$', id)
        if match:
            return super().__new__(cls, 'tt' + match.group(1).rjust(7, '0'))
        else:
            raise argtypes.ArgumentTypeError(f'Invalid IMDb ID: {id}')


class PtpTrackerConfig(TrackerConfigBase):
    defaults = {
        'base_url': base64.b64decode('aHR0cHM6Ly9wYXNzdGhlcG9wY29ybi5tZQ==').decode('ascii'),
        'username': '',
        'password': '',
        'announce_url': configfiles.config_value(
            value='',
            description='Your personal announce URL.',
        ),
        'image_host': configfiles.config_value(
            value=types.ListOf(
                item_type=PtpImageHost,
                default=('ptpimg', 'imgbox'),
                separator=',',
            ),
            description=(
                'List of image hosting service names. The first service is normally used '
                'with the others as backup if uploading to the first fails.\n'
                + 'Supported services: ' + ', '.join(PtpImageHost.options)
            ),
        ),
        'screenshots_from_movie': configfiles.config_value(
            value=types.Integer(3, min=3, max=10),
            description='How many screenshots to make for single-video uploads.',
        ),
        'screenshots_from_episode': configfiles.config_value(
            value=types.Integer(2, min=2, max=10),
            description='How many screenshots to make per video for multi-video uploads.',
        ),
        'exclude': (
            exclude.checksums,
            exclude.images,
            exclude.nfo,
            exclude.samples,
        ),
    }

    argument_definitions = {
        'submit': {
            ('--hardcoded-subtitles', '--hs'): {
                'help': 'Video contains hardcoded subtitles',
                'action': 'store_true',
            },
            ('--no-english-subtitles', '--nes'): {
                'help': (
                    'Whether release contains no English audio and no English subtitles.'
                    '\n'
                    'This is autodetected reliably if all audio and subtitle tracks have '
                    'a correct language tag. If not, you are asked interactively.\n'
                    'Subtitle languages are detected in *.idx/sub, VIDEO_TS trees '
                    'and *.srt/ssa/ass/vtt by language code in the file name, e.g. '
                    '"Foo.en.srt".'
                ),
                'metavar': 'BOOL',
                'type': argtypes.bool_or_none,
            },
            ('--not-main-movie', '--nmm'): {
                'help': 'Upload ONLY contains extras, Rifftrax, Workprints',
                'action': 'store_true',
            },
            ('--personal-rip', '--pr'): {
                'help': 'Tag as your own encode',
                'action': 'store_true',
            },
            ('--poster', '--po'): {
                'help': 'Path or URL to movie poster',
            },
            ('--imdb', '--im'): {
                'help': 'IMDb ID or URL',
                'type': PtpImdbId,
            },
            ('--source', '--so'): {
                'help': (
                    'Original source of this release\n'
                    + 'Should vaguely match: '
                    + ', '.join(metadata.sources)
                ),
            },
            ('--type', '--ty'): {
                'help': (
                    'General category of this release\n'
                    + 'Must vaguely match: '
                    + ', '.join(metadata.types)
                ),
                'type': PtpReleaseType,
            },
            ('--screenshots', '--ss'): {
                'help': 'How many screenshots to make per video file',
                'type': argtypes.number_of_screenshots(min=1, max=10),
            },
            ('--upload-token', '--ut'): {
                'help': 'Upload token from staff',
            },
            ('--only-description', '--od'): {
                'help': 'Only generate description (do not upload anything)',
                'action': 'store_true',
                'group': 'generate-metadata',
            },
        },
    }
