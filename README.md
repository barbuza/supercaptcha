supercaptcha
============

supercaptcha is easy to use captcha field for [django](http://code.djangoproject.com/) newforms

mercurial repo and tickets available at [bitbucket](http://bitbucket.org/barbuza/supercaptcha)

Usage
-----

    class MySuperForm(forms.Form):
        ...
        captcha = supercaptcha.CaptchaField(label=u'no robots here')
        ...


Requirements
------------

You don't need any changes in form, or middleware or context processor or other boring things.

All you need, to get captcha working is properly configured cache backend and view added to urlconf:
	
    url(r'^captcha/(?P<code>[\da-f]{32})/$', 'supercaptcha.draw')

And, surely, PIL library installed.


Configuration
-------------

All these options should be used in settings of your project

#### CAPTCHA\_SYMBOLS
string with all symbols, which should be used in captcha, default is `'123456789ABCDEFGHJKLMNPQRSTVXYZ'`

#### CAPTCHA\_LENGTH
length if captcha code, default is `6`

#### CAPTCHA\_FONTS
the tuple of tuples with name - fullpath pair for each font which should be used

#### CAPTCHA\_FOREGROUND\_COLORS
tuple of tuples with colors for text. use one if if you want single color, for example `((0,0,0),)` for black color

#### CAPTCHA\_COLORIZE\_SYMBOLS
whould we use different colors for each symbol default is `True`

#### CAPTCHA\_BACKGROUND\_COLOR
background color, deafult is `(255, 255, 255)`
 
#### CAPTCHA\_FILTER\_CHAIN
PIL filters, for example `('BLUR', 'SHARPEN',)` default is `[]`

#### CAPTCHA\_VERTICAL\_JUMP
defines if letters should "jump", default is `True`

#### CAPTCHA\_SIZE
tuple defining size of captcha image, default is `(200, 100)`

#### CAPTCHA\_ALT
"alt" for image tag, default is `'no robots here'`

#### CAPTCHA\_FORMAT
controls which format will be used for image encoding, default is `('JPEG', 'image/jpeg')`

#### CAPTCHA\_CACHE\_PREFIX
defines which prefix should supercaptcha use for dealing with cache, default is `'captcha'`

#### CAPTCHA\_DEFAULT\_ERROR\_MESSAGE
defines default error message for wrong code

#### CAPTCHA\_REFRESH
defines if CaptchaField should show refresh link, default is `False`

#### CAPTCHA\_REFRESH\_LINK\_TEXT
defines text of refresh link

#### CAPTCHA\_HTML\_TEMPLATE
defines template of CaptchaField, see example in settings

#### CAPTCHA\_HTML\_TEMPLATE\_WITH\_REFRESH
defines template of CaptchaField with refresh link, see example in settings