.. supercaptcha documentation master file, created by
   sphinx-quickstart on Tue Apr 26 00:44:41 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

supercaptcha
============

supercaptcha is easy to use captcha field for `django <http://code.djangoproject.com/>`_ newforms

git repo is available at `github <http://github.com/barbuza/supercaptcha>`_

mercurial repo is available at `bitbucket <http://bitbucket.org/barbuza/supercaptcha>`_

*****
Usage
*****
::

   class MySuperForm(forms.Form):
       ...
       captcha = supercaptcha.CaptchaField(label=u'no robots here')
       ...


************
Requirements
************

You don't need any changes in form, or middleware or context processor or other boring things.

All you need, to get captcha working is properly configured cache backend and view added to urlconf:
::

   url(r'^captcha/(?P<code>[\da-f]{32})/$', 'supercaptcha.draw')

And, surely, PIL library installed.


*************
Configuration
*************

All these options should be used in settings of your project

CAPTCHA_SYMBOLS
"""""""""""""""
string with all symbols, which should be used in captcha, default is ``'123456789ABCDEFGHJKLMNPQRSTVXYZ'``

CAPTCHA_LENGTH
""""""""""""""
length if captcha code, default is ``6``

CAPTCHA_FONTS
"""""""""""""
the tuple of tuples with name - fullpath pair for each font which should be used

CAPTCHA_FOREGROUND_COLORS
"""""""""""""""""""""""""
tuple of tuples with colors for text. use one if if you want single color, for example ``((0,0,0),)`` for black color

CAPTCHA_COLORIZE_SYMBOLS
""""""""""""""""""""""""
whould we use different colors for each symbol default is ``True``

CAPTCHA_BACKGROUND_COLOR
""""""""""""""""""""""""
background color, deafult is ``(255, 255, 255)``

CAPTCHA_FILTER_CHAIN
""""""""""""""""""""
PIL filters, for example ``('BLUR', 'SHARPEN',)`` default is ``[]``

CAPTCHA_VERTICAL_JUMP
"""""""""""""""""""""
defines if letters should "jump", default is ``True``

CAPTCHA_SIZE
""""""""""""
tuple defining size of captcha image, default is ``(200, 100)``

CAPTCHA_ALT
"""""""""""
"alt" for image tag, default is ``'no robots here'``

CAPTCHA_FORMAT
""""""""""""""
controls which format will be used for image encoding, default is ``('JPEG', 'image/jpeg')``

CAPTCHA_CACHE_PREFIX
""""""""""""""""""""
defines which prefix should supercaptcha use for dealing with cache, default is ``'captcha'``

CAPTCHA_DEFAULT_ERROR_MESSAGE
"""""""""""""""""""""""""""""
defines default error message for wrong code

CAPTCHA_REFRESH
"""""""""""""""
defines if CaptchaField should show refresh link, default is ``False``

CAPTCHA_REFRESH_LINK_TEXT
"""""""""""""""""""""""""
defines text of refresh link

CAPTCHA_HTML_TEMPLATE
"""""""""""""""""""""
defines template of CaptchaField, see example in settings

CAPTCHA_HTML_TEMPLATE_WITH_REFRESH
""""""""""""""""""""""""""""""""""
defines template of CaptchaField with refresh link, see example in settings

.. toctree::
   :maxdepth: 2

Indices and tables
==================

* :ref:`genindex`
* :ref:`search`

