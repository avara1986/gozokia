# encoding: utf-8
from __future__ import absolute_import, print_function, unicode_literals
import os
from gozokia.i_o import Io
from gozokia.conf import settings


class Gozokia:
    '''
    GOZOKIA_DIR: The directory where gozokia have been calling.
    '''
    GOZOKIA_DIR = os.path.dirname(os.path.abspath(__file__))

    '''
    PROJECT_DIR: The directory where the project is running.
    '''
    PROJECT_DIR = os.getcwd()

    def __init__(self):
        self.set_io(input_type=settings.GOZOKIA_INPUT_TYPE,
                    output_type=settings.GOZOKIA_OUTPUT_TYPE,
                    )

    def set_io(self, *args, **kwargs):
        self.io = Io(*args, **kwargs)

    def console(self):
        input_result = True
        while input_result is not False:
            input_result = self.io.listen()

            # TODO: Get logic here
            output_result = "you said: {}".format(input_result)

            self.io.response(output_result)
