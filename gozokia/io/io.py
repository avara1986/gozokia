# encoding: utf-8
"""
I/O configurations
"""
import subprocess
import urllib.request
import importlib


class GozokiaIoError(Exception):
    '''raise this when there's a lookup error for my app'''


class Io(object):
    _LANGUAGE = "es-ES"
    """
    INPUT
    """
    _METHOD_DEFAULT = "terminal_txt"
    """
    OUTPUT
    """
    _VALUE = 0
    _TXT = 1
    _VOICE = 2
    _TXT_VOICE = 3

    _INPUT_METHODS = {"value": _VALUE, "terminal_txt": _TXT, "terminal_voice": _VOICE}
    _OUTPUT_METHODS = {"value": _VALUE, "terminal_txt": _TXT, "terminal_voice": _VOICE, "terminal_txtvoice": _TXT_VOICE}
    _INPUT_SELECTED = 0
    _OUTPUT_SELECTED = 0
    # System program to play sounds
    # _AUDIO_PLAYER = "mpg123"

    def __init__(self, *args, **kwargs):
        self.set_input_method(kwargs.get('input_type', self._METHOD_DEFAULT))
        self.set_output_method(kwargs.get('output_type', self._METHOD_DEFAULT))
        # s self.set_audio_player(kwargs.get('audio_player', self._AUDIO_PLAYER))

    '''
    Input configuration
    '''
    def set_input_method(self, input_type):
        try:
            self._INPUT_SELECTED = self._INPUT_METHODS[input_type]
        except KeyError:
            raise GozokiaIoError(__class__.__name__ + ": Input method {} not exist".format(input_type))

        # Initialize the input method
        input_module = importlib.import_module('gozokia.io.input')
        if self._INPUT_SELECTED == self._VALUE:
            self.input = input_module.InputValue()
        elif self._INPUT_SELECTED == self._TXT:
            self.input = input_module.InputTerminalText()
        elif self._INPUT_SELECTED == self._VOICE:
            self.input = input_module.InputTerminalVoice()

    def get_input_method(self):
        return self._INPUT_SELECTED

    def listen(self, *args, **kwargs):
        input_result = self.input.listen(*args, **kwargs)
        if len(input_result) == 0:
            input_result = False
        return input_result

    '''
    Output configuration
    '''
    def set_output_method(self, output_type):
        try:
            self._OUTPUT_SELECTED = self._OUTPUT_METHODS[output_type]
        except KeyError:
            raise GozokiaIoError(__class__.__name__ + ": Output method {} not exist".format(output_type))
        output_module = importlib.import_module('gozokia.io.output')
        if self._OUTPUT_SELECTED == self._VALUE:
            self.output = output_module.OutputValue()
        elif self._OUTPUT_SELECTED == self._TXT:
            self.output = output_module.OutputTerminalText()
        elif self._OUTPUT_SELECTED == self._VOICE:
            self.output = output_module.OutputTerminalVoice()

    def get_output_method(self):
        return self._OUTPUT_SELECTED

    def response(self, text):
        return self.output.response(response=text)
