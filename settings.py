# -*- coding: utf-8 -*-
from os.path import join, dirname, abspath

from django.conf import settings


SELF_DIR = dirname(abspath(__file__))
FONTS_DIR = join(SELF_DIR, 'fonts')

SYMBOLS = getattr(settings, 'CAPTCHA_SYMBOLS', '123456789ABCDEFGHJKLMNOPQRSTVXYZ')
LENGTH = getattr(settings, 'CAPTCHA_LENGTH', 6)

AVAIL_FONTS = getattr(settings, 'CAPTCHA_FONTS', [
    (join(FONTS_DIR, 'WCManoNegraBta.ttf'), 29),
    (join(FONTS_DIR, 'Diavlo_LIGHT_II_37.otf'), 29),
    (join(FONTS_DIR, 'ZebraPrint.ttf'), 23),
    (join(FONTS_DIR, 'Acidic.ttf'), 30),
    (join(FONTS_DIR, 'ADLOCK.ttf'), 27)
])

START_POSITION = getattr(settings, 'CAPTCHA_START_POSITION', (5, 1))
FOREGROUND_COLOR = getattr(settings, 'CAPTCHA_FOREGROUND_COLOR', (133, 7, 8))
BACKGROUND_COLOR = getattr(settings, 'CAPTCHA_BACKGROUND_COLOR', (255, 255, 255))
FILTER_CHAIN = getattr(settings, 'CAPTCHA_FILTER_CHAIN', ('SHARPEN', ))
MAX_IMAGE_WIDTH = 180

WIDTH = getattr(settings, 'CAPTCHA_WIDTH', 180)
HEIGHT = getattr(settings, 'CAPTCHA_HEIGHT', 60)
ALT = getattr(settings, 'CAPTCHA_ALT', 'secret code')
