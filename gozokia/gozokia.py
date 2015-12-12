# encoding: utf-8
import os
import sys
sys.path.insert(0, os.getcwd())

from .io import Io

class Gozokia:
    def __init__(self):
        self.set_language('es-ES')
        self.set_io(input_type=os.environ.get('GOZOKIA_INPUT_TYPE'),
                    output_type=os.environ.get('GOZOKIA_OUTPUT_TYPE'),
                    # audio_player=os.environ.get('GOZOKIA_AUDIO_PLAYER')
                    )

    def set_io(self, *args, **kwargs):
        self.io = Io(*args, **kwargs)

    def set_language(self, language=None):
        if language is None:
            language = os.environ["GOZOKIA_LANGUAGE"]
        self._LANGUAGE = language

    def get_language(self):
        return self._LANGUAGE

    def console(self):
        input_result = True
        while input_result != False:
            input_result = self.io.listen(language=self.get_language())

            # TODO: Get logic here
            output_result = "you said: {}".format(input_result)

            self.io.response(output_result)
