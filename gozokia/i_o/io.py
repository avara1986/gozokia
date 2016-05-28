# encoding: utf-8
"""
I/O configurations
"""
from __future__ import absolute_import, print_function, unicode_literals
import importlib
from gozokia.i_o.exceptions import GozokiaIoError
from gozokia.conf import settings


class Io(object):
    _VALUE = 0
    _TXT = 1
    _VOICE = 2
    _TXT_VOICE = 3
    _METHOD_DEFAULT = "terminal_txt"
    """
    INPUT
    """
    _INPUT_METHODS = {"value": _VALUE, "terminal_txt": _TXT, "terminal_voice": _VOICE}
    _INPUT_SELECTED = 0
    """
    OUTPUT
    """
    _OUTPUT_METHODS = {"value": _VALUE, "terminal_txt": _TXT, "terminal_voice": _VOICE, "terminal_txtvoice": _TXT_VOICE}
    _OUTPUT_SELECTED = 0
    # System program to play sounds
    # _AUDIO_PLAYER = "mpg123"

    def __init__(self, *args, **kwargs):
        self.set_input_method(kwargs.get('input_type', settings.GOZOKIA_INPUT_TYPE))
        self.set_output_method(kwargs.get('output_type', settings.GOZOKIA_OUTPUT_TYPE))

    '''
    Input configuration
    '''

    def set_input_method(self, input_type):
        try:
            self._INPUT_SELECTED = self._INPUT_METHODS[input_type]
        except KeyError:
            raise GozokiaIoError(__class__.__name__ + ": Input method {} not exist".format(input_type))

        # Initialize the input method
        input_module = importlib.import_module('gozokia.i_o.input')
        if self._INPUT_SELECTED == self._VALUE:
            self.input = input_module.InputValue()
        elif self._INPUT_SELECTED == self._TXT:
            self.input = input_module.InputTerminalText()
        elif self._INPUT_SELECTED == self._VOICE:
            self.input = input_module.InputTerminalVoice()

    def get_input_method(self):
        return self._INPUT_SELECTED

    def listen(self, *args, **kwargs):
        return self.input.listen(*args, **kwargs)

    '''
    Output configuration
    '''

    def set_output_method(self, output_type):
        try:
            self._OUTPUT_SELECTED = self._OUTPUT_METHODS[output_type]
        except KeyError:
            raise GozokiaIoError(__class__.__name__ + ": Output method {} not exist".format(output_type))
        output_module = importlib.import_module('gozokia.i_o.output')
        if self._OUTPUT_SELECTED == self._VALUE:
            self.output = output_module.OutputValue()
        elif self._OUTPUT_SELECTED == self._TXT:
            self.output = output_module.OutputTerminalText()
        elif self._OUTPUT_SELECTED == self._VOICE:
            self.output = output_module.OutputTerminalVoice()

    def get_output_method(self):
        return self._OUTPUT_SELECTED

    def response(self, text, *args, **kwargs):
        return self.output.response(response=text, *args, **kwargs)
