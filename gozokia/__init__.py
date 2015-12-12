# encoding: utf-8

'''
Default settings of Gozokia.
Its coulds be defined on your Django settings
'''
import os
from .gozokia import Gozokia

__author__ = "Alberto Vara"
__email__ = "a.vara.1986@gmail.com"
__version__ = "0.2"
__license__ = "MIT"

if os.environ.get('GOZOKIA_INPUT_TYPE') is None:
    os.environ["GOZOKIA_INPUT_TYPE"] = "terminal_txt"
if os.environ.get('GOZOKIA_OUTPUT_TYPE') is None:
    os.environ["GOZOKIA_OUTPUT_TYPE"] = "terminal_txt"
if os.environ.get('GOZOKIA_AUDIO_PLAYER') is None:
    os.environ["GOZOKIA_AUDIO_PLAYER"] = "mpg123"
if os.environ.get('GOZOKIA_LANGUAGE') is None:
    os.environ["GOZOKIA_LANGUAGE"] = "en-US"