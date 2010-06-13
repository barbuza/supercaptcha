# -*- coding: utf-8 -*-

import os
from random import choice, random

try:
    import Image, ImageDraw, ImageFont, ImageFilter
except ImportError:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
from django import forms
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.forms.util import flatatt
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy
from django.views.decorators.cache import never_cache

import settings


try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local

_thread_locals = local()


WIDTH = settings.SIZE[0]
HEIGHT = settings.SIZE[1]
SYMBOLS = ugettext_lazy(settings.SYMBOLS)
LENGTH = settings.LENGTH
BG_COLOR = settings.BACKGROUND_COLOR
FG_COLORS = settings.FOREGROUND_COLORS
ENC_TYPE, MIME_TYPE = settings.FORMAT
JUMP = settings.VERTICAL_JUMP
COLORIZE = settings.COLORIZE_SYMBOLS
PREFIX = settings.CACHE_PREFIX
CODE_ATTR_NAME = '_captcha_code'
ERROR_MESSAGE = settings.DEFAULT_ERROR_MESSAGE
HTML_TEMPLATE = settings.HTML_TEMPLATE
HTML_TEMPLATE_WITH_REFRESH = settings.HTML_TEMPLATE_WITH_REFRESH
REFRESH = settings.REFRESH
REFRESH_LINK_TEXT = ugettext_lazy(settings.REFRESH_LINK_TEXT)


def get_current_code():
    if not hasattr(_thread_locals, CODE_ATTR_NAME):
        code = os.urandom(16).encode('hex')
        setattr(_thread_locals, CODE_ATTR_NAME, code)
    return getattr(_thread_locals, CODE_ATTR_NAME)


def set_current_code(value):
    setattr(_thread_locals, CODE_ATTR_NAME, value)


def empty_current_code():
    if hasattr(_thread_locals, CODE_ATTR_NAME):
        delattr(_thread_locals, CODE_ATTR_NAME)


def generate_text():
    return ''.join([choice(SYMBOLS) for _ in range(LENGTH)])


@never_cache
def draw(request, code):
    
    font_name, fontfile = choice(settings.AVAIL_FONTS)
    cache_name = '%s-%s-size' % (PREFIX, font_name)
    text = generate_text()
    cache.set('%s-%s' % (PREFIX, code), text, 600)
    
    def fits(font_size):
        font = ImageFont.truetype(fontfile, font_size)
        size = font.getsize(text)
        return size[0] < WIDTH and size[1] < HEIGHT
    
    font_size = cache.get(cache_name , 10)
    if fits(font_size):
        while True:
            font_size += 1
            if not fits(font_size):
                font_size -= 1
                break
    else:
        while True:
            font_size -= 1
            if fits(font_size):
                break
    cache.set(cache_name, font_size, 600)
    
    font = ImageFont.truetype(fontfile, font_size)
    text_size = font.getsize(text)
    icolor = 'RGB'
    if len(BG_COLOR) == 4:
        icolor = 'RGBA'
    im = Image.new(icolor, (WIDTH, HEIGHT), BG_COLOR)
    d = ImageDraw.Draw(im)
    if JUMP:
        if COLORIZE:
            get_color = lambda: choice(FG_COLORS)
        else:
            color = choice(FG_COLORS)
            get_color = lambda: color
        position = [(WIDTH - text_size[0]) / 2, 0]
        shift_max = HEIGHT - text_size[1]
        shift_min = shift_max / 4
        shift_max = shift_max * 3 / 4
        for char in text:
            l_size = font.getsize(char)
            try:
                position[1] = choice(range(shift_min, shift_max + 1))
            except IndexError:
                position[1] = shift_min
            d.text(position, char, font=font, fill=get_color())
            position[0] += l_size[0]
    else:
        position = [(WIDTH - text_size[0]) / 2,
                    (HEIGHT - text_size[1]) / 2]
        d.text(position, text, font=font, fill=choice(FG_COLORS))
    
    response = HttpResponse(mimetype=MIME_TYPE)
    
    response['cache-control'] = 'no-store, no-cache, must-revalidate, proxy-revalidate'
    
    for f in settings.FILTER_CHAIN:
        im = im.filter(getattr(ImageFilter, f))
    
    im.save(response, ENC_TYPE)
    return response

class CaptchaImageWidget(forms.Widget):
    
    if REFRESH:
        template = HTML_TEMPLATE_WITH_REFRESH
    else:
        template = HTML_TEMPLATE
    
    def render(self, name, value, attrs=None):
        code = get_current_code()
        empty_current_code()
        input_attrs = self.build_attrs(attrs, type='text', name=name)
        src = reverse(draw, kwargs={'code': code})
        return mark_safe(self.template % {'src': src, 'input_attrs': flatatt(input_attrs),
                                          'alt': settings.ALT, 'width': WIDTH, 'length': LENGTH,
                                          'height': HEIGHT, 'rnd': random(),
                                          'refresh_text': REFRESH_LINK_TEXT})

class HiddenCodeWidget(forms.HiddenInput):
	
    def render(self, name, value=None, attrs=None):
        if value is None:
            empty_current_code()
        if not value:
            value = get_current_code()
        else:
            set_current_code(value)
        return super(HiddenCodeWidget, self).render(name, value, attrs=attrs)


class CaptchaWidget(forms.MultiWidget):
    
    def __init__(self, attrs={}, code=None):
        widgets = (HiddenCodeWidget(attrs=attrs), CaptchaImageWidget(attrs=attrs))
        super(CaptchaWidget, self).__init__(widgets, attrs)
    
    def decompress(self, value):
        if value:
            return value.split()
        return [None, None]

    @classmethod
    def id_for_label(cls, id_):
        if id_:
            id_ += '_1'
        return id_


class CaptchaField(forms.MultiValueField):
    
    widget = CaptchaWidget

    default_error_messages = {
        'wrong': ugettext_lazy(ERROR_MESSAGE),
        'required': ugettext_lazy(u'This field is required.'),
        'internal': ugettext_lazy(u'Internal error.'),
        }

    def __init__(self, *args, **kwargs):
        fields = (
            forms.CharField(max_length=32, min_length=32),
            forms.CharField(max_length=settings.LENGTH, min_length=settings.LENGTH),
            )
        super(CaptchaField, self).__init__(fields, *args, **kwargs)
        
    def compress(self, data_list):
        return ' '.join(data_list)
    
    def clean(self, value):
        if len(value) != 2:
            raise forms.ValidationError, self.error_messages['wrong']
        
        code, text = value
        cached_text = cache.get('%s-%s' % (PREFIX, code))
        cache.set('%s-%s' % (PREFIX, code), generate_text(), 600)
        
        if not cached_text:
            raise forms.ValidationError, self.error_messages['internal']
        if not text:
            raise forms.ValidationError, self.error_messages['required']
        if text.lower() != cached_text.lower():
            raise forms.ValidationError, self.error_messages['wrong']
        
