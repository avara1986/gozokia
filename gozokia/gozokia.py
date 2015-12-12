# encoding: utf-8
import os
from gozokia.io import Io

INPUT_TYPE = "txt"
OUTPUT_TYPE = "txt"
AUDIO_PLAYER = 'mpg123'

class Gozokia:
    def __init__(self):
        self.set_io(input_type=os.environ.get('GOZOKIA_INPUT_TYPE'), output_type=os.environ.get('GOZOKIA_OUTPUT_TYPE'), audio_player=os.environ.get('GOZOKIA_AUDIO_PLAYER'))
    
    def set_io(self, *args, **kwargs):
        self.io = Io(*args, **kwargs)
    
    def console(self):
        input_result = True
        while input_result != False:
            '''
            Get the audio or text input and return it
            '''
            input_result = self.io.listen()
            print("you said: {}".format(input_result))