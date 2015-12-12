# encoding: utf-8

"""Library for personal assistans."""

__author__ = "Alberto Vara"
__version__ = "0.2"
__license__ = "MIT"
import os
from .gozokia import Gozokia

if os.environ.get('GOZOKIA_INPUT_TYPE') is None:
    os.environ["GOZOKIA_INPUT_TYPE"] = "txt"
if os.environ.get('GOZOKIA_OUTPUT_TYPE') is None:
    os.environ["GOZOKIA_OUTPUT_TYPE"] = "txt"
if os.environ.get('GOZOKIA_AUDIO_PLAYER') is None:
    os.environ["GOZOKIA_AUDIO_PLAYER"] = "mpg123"