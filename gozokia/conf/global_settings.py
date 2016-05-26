DEBUG = False

GOZOKIA_INPUT_TYPE = "terminal_txt"
GOZOKIA_OUTPUT_TYPE = "terminal_txt"
GOZOKIA_AUDIO_PLAYER = "mpg123"
GOZOKIA_LANGUAGE = "en-US"

GOZOKIA_TEXT_ANALYZER_ENGINE = False

DATABASES = {
    'default': {
        'ENGINE': 'gozokia.db.backends.memory',
        'NAME': 'gozokia',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
