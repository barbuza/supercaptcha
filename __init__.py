# -*- coding: utf-8 -*-
from random import choice, random
from uuid import uuid4

import Image, ImageDraw, ImageFont, ImageFilter
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


CODE_ATTR_NAME = '_captcha_code'


def get_current_code():
    if not hasattr(_thread_locals, CODE_ATTR_NAME):
        code = uuid4().get_hex()
        setattr(_thread_locals, CODE_ATTR_NAME, code)
    return getattr(_thread_locals, CODE_ATTR_NAME)


def set_current_code(value):
    setattr(_thread_locals, CODE_ATTR_NAME, value)


def empty_current_code():
    if hasattr(_thread_locals, CODE_ATTR_NAME):
        delattr(_thread_locals, CODE_ATTR_NAME)


def generate_text():
    return ''.join([choice(settings.SYMBOLS) for _ in range(settings.LENGTH)])


@never_cache
def draw(request, code):
    
    curr_font = choice(settings.AVAIL_FONTS)
    fontsize = choice(range(curr_font[1] - 3, curr_font[1]))
    text = generate_text()
    cache.set('captcha-%s' % code, text, 600)
    
    def get_image_size(fontname, fontsize, text, max_width):
        font = ImageFont.truetype(fontname, fontsize)
        img_size = list(font.getsize(text))
        img_size[0] += settings.LENGTH * 4 + settings.START_POSITION[0]
        img_size[1] +=15
        while img_size[0] > max_width:
            fontsize -= 1
            font = ImageFont.truetype(fontname, fontsize)
            img_size = list(font.getsize(text))
            img_size[0] += settings.LENGTH * 4 + settings.START_POSITION[0]
            img_size[1] += 15
        return font, Image.new('RGB', img_size, settings.BACKGROUND_COLOR)

    font, im = get_image_size(curr_font[0], fontsize, text, settings.MAX_IMAGE_WIDTH)

    d = ImageDraw.Draw(im)
    position = list(settings.START_POSITION)
    for char in text:
        l_size = font.getsize(char)
        position[1] = choice(range(1, 15))
        d.text(position, char, font=font,
               fill=settings.FOREGROUND_COLOR)
        position[0] += l_size[0] + 2
     
    response = HttpResponse(mimetype='image/gif')
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, proxy-revalidate'
    for f in settings.FILTER_CHAIN:
        im = im.filter(getattr(ImageFilter, f))
    im.rotate(45)
    im.save(response, "GIF")
    return response

class CaptchaImageWidget(forms.Widget):
    
    template = '<img src="%(src)s?%(rnd)s" alt="%(alt)s" width="%(width)s" height="%(height)s" /><input%(input_attrs)s />'
    
    
    def render(self, name, value, attrs=None):
        code = get_current_code()
        empty_current_code()
        input_attrs = self.build_attrs(attrs, type='text', name=name)
        src = reverse(draw, kwargs={'code': code})
        return mark_safe(self.template % {'src': src, 'input_attrs': flatatt(input_attrs),
                                          'alt': settings.ALT, 'width': settings.WIDTH,
                                          'height': settings.HEIGHT, 'rnd': random()})

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



class CaptchaField(forms.MultiValueField):
    
    widget = CaptchaWidget

    default_error_messages = {
        'wrong': ugettext_lazy(u'The code you entered is wrong.'),
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
        cached_text = cache.get('captcha-%s' % code)
        cache.set('captcha-%s' % code, generate_text(), 600)
        
        if not cached_text:
            raise forms.ValidationError, self.error_messages['internal']
        if not text:
            raise forms.ValidationError, self.error_messages['required']
        if text.lower() != cached_text.lower():
            raise forms.ValidationError, self.error_messages['wrong']
        
