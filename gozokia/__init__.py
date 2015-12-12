# encoding: utf-8

"""Library for personal assistans."""

__author__ = "Alberto Vara"
__version__ = "0.2"
__license__ = "MIT"

from gozokia.ino import Io

INPUT_TYPE = "txt"
OUTPUT_TYPE = "txt"
AUDIO_PLAYER = 'mpg123'


class Gozokia:
    def __init__(self):
        self.ino = Io(input_type=INPUT_TYPE, output_type=OUTPUT_TYPE, audio_player=AUDIO_PLAYER)
        input_result = True
        while input_result != False:
            '''
            Get the audio or text input and return it
            '''
            input_result = self.ino.listen()
            print("you said: {}".format(input_result))