# -*- coding: utf-8 -*-
from os.path import join, dirname, abspath

from django.conf import settings


SELF_DIR = dirname(abspath(__file__))
FONTS_DIR = join(SELF_DIR, 'fonts')

SYMBOLS = getattr(settings, 'CAPTCHA_SYMBOLS', '123456789ABCDEFGHJKLMNPQRSTVXYZ')
LENGTH = getattr(settings, 'CAPTCHA_LENGTH', 6)

AVAIL_FONTS = getattr(settings, 'CAPTCHA_FONTS', [
        ('boneca', join(FONTS_DIR, 'boneca.ttf')),
        ('acidic', join(FONTS_DIR, 'acidic.ttf')),
])

FOREGROUND_COLORS = getattr(settings, 'CAPTCHA_FOREGROUND_COLORS', (
        (0, 0, 0),
        (0x77, 0, 0),
        (0, 0x77, 0),
        (0, 0, 0x77),
        ))

COLORIZE_SYMBOLS = getattr(settings, 'CAPTCHA_COLORIZE_SYMBOLS', True)

BACKGROUND_COLOR = getattr(settings, 'CAPTCHA_BACKGROUND_COLOR', (255, 255, 255))

FILTER_CHAIN = getattr(settings, 'CAPTCHA_FILTER_CHAIN', [])

VERTICAL_JUMP = getattr(settings, 'CAPTCHA_VERTICAL_JUMP', True)

SIZE = getattr(settings, 'CAPTCHA_SIZE', (200, 100))
ALT = getattr(settings, 'CAPTCHA_ALT', 'no robots here')
FORMAT = getattr(settings, 'CAPTCHA_FORMAT', ('JPEG', 'image/jpeg'))

CACHE_PREFIX = getattr(settings, 'CAPTCHA_CACHE_PREFIX', 'captcha')
