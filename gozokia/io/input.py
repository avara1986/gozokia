import sys
import speech_recognition as sr
from .io_base import InputBase

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
    
class InputTerminalVoice(InputBase):
    
    def listen(self, *args, **kwargs):
        super(InputTerminalVoice, self).listen(*args, **kwargs)
        # use the default microphone as the audio source
        with sr.Microphone() as source:
            # listen for the first phrase and extract it into audio data
            input_audio = self._recognizer_r.listen(source)
        try:
            # using Google Speech Recognition
            input_result = self._recognizer_r.recognize(input_audio).lower()
            input_result = input_result.encode('utf8')

        # speech is unintelligible
        except LookupError:
            print("I don't understand you")
            input_result = False
        return input_result