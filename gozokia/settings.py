import os
if os.environ.get('GOOGLE_TRANSLATE_KEY') is None:
    os.environ["GOOGLE_TRANSLATE_KEY"] = "AIzaSyDdSAATt2NNE09AiQGgEPn-GXSgM3iuyPE"
if os.environ.get('GOZOKIA_INPUT_TYPE') is None:
    os.environ["GOZOKIA_INPUT_TYPE"] = "terminal_txt"
if os.environ.get('GOZOKIA_OUTPUT_TYPE') is None:
    os.environ["GOZOKIA_OUTPUT_TYPE"] = "terminal_txt"
if os.environ.get('GOZOKIA_AUDIO_PLAYER') is None:
    os.environ["GOZOKIA_AUDIO_PLAYER"] = "mpg123"
if os.environ.get('GOZOKIA_LANGUAGE') is None:
    os.environ["GOZOKIA_LANGUAGE"] = "en-US"