#!/usr/bin/env python
# encoding: utf-8

"""Library for personal assistans."""

__author__ = "Alberto Vara"
__version__ = "0.2"
__license__ = "MIT"

from ino import Io

INPUT_TYPE = "txt"
OUTPUT_TYPE = "txt"
AUDIO_PLAYER = 'mpg123'


class Gozokia:

    def __init__(self, input_type="txt"):
        self.ino = Io(
            input_type=INPUT_TYPE, output_type=OUTPUT_TYPE, audio_player=AUDIO_PLAYER)
        input_result = True
        '''
        self.cs = CommandSystem(
            input_type=INPUT_TYPE, output_type=OUTPUT_TYPE, audio_player=AUDIO_PLAYER)
        
        self.chat = Chat(
            input_type=INPUT_TYPE, output_type=OUTPUT_TYPE, audio_player=AUDIO_PLAYER)
        '''
        while input_result != False:
            '''
            Get the audio or text input and return it
            '''
            input_result = self.ino.listen()
            print("you said: {}".format(input_result))
            #input_result = self.cs.execute(input_result)
            #input_result = self.chat.execute(input_result)

if __name__ == '__main__':
    print('\n*** Gozokia ***')
    Gozokia()
