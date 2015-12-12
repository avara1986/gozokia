import sys

from .io_base import InputBase
from .io_voice import VoiceRecognizerMixin


class InputTerminalText(InputBase):

    def listen(self, *args, **kwargs):
        super(InputTerminalText, self).listen(*args, **kwargs)
        """
        Normalize reading input between python 2 and 3.
        'raw_input' is just 'input' in python3
        https://github.com/gunthercox/ChatterBot/blob/master/chatterbot/utils/read_input.py
        """
        if sys.version_info[0] < 3:
            input_text = str(raw_input("> "))
        else:
            input_text = input("> ")
        return input_text


class InputValue(InputBase):

    def listen(self, *args, **kwargs):
        super(InputValue, self).listen(*args, **kwargs)
        if 'value' in kwargs:
            return kwargs.pop('value')
        return ""


class InputTerminalVoice(InputBase, VoiceRecognizerMixin):

    def __init__(self, *args, **kwargs):
        super(InputTerminalVoice, self).__init__(*args, **kwargs)
        self.set_voice_recognizer()

    def listen(self, *args, **kwargs):
        language = kwargs.get('language', "en-US")
        super(InputTerminalVoice, self).listen(*args, **kwargs)
        self.set_voice_recognizer()
        input_result = self.listen_audio(language)
        return input_result
