import sys
import os
from gozokia.i_o.io_base import OutputBase
from gozokia.i_o.io_voice import VoiceResponseMixin


class OutputTerminalText(OutputBase):

    def response(self, *args, **kwargs):
        super(OutputTerminalText, self).response(*args, **kwargs)
        print("- Gozokia: ", kwargs.get('response', ""))
        return True


class OutputValue(OutputBase):

    def response(self, *args, **kwargs):
        super(OutputValue, self).response(*args, **kwargs)
        return kwargs.get('response', "")


class OutputTerminalVoice(OutputBase, VoiceResponseMixin):

    def __init__(self, *args, **kwargs):
        super(OutputTerminalVoice, self).__init__(*args, **kwargs)

    def response(self, *args, **kwargs):
        language = kwargs.get('language', os.environ.get("GOZOKIA_LANGUAGE"))
        super(OutputTerminalVoice, self).response(*args, **kwargs)
        self.response_speak(kwargs.get('response', ""), language=language)
        return True
