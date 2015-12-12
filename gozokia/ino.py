# encoding: utf-8
"""
I/O configurations
"""

__author__ = "Alberto Vara"
__version__ = "0.2"
__license__ = "MIT"

import speech_recognition as sr
import subprocess
import urllib.request


class Io(object):
    _LANGUAGE = "es-ES"
    """
    RESPONSES
    """
    _VALUE = 0
    _TXT = 1
    _VOICE = 2
    _TXT_VOICE = 3

    _INPUT_METHODS = {"value": _VALUE, "txt": _TXT, "voice": _VOICE}
    _OUTPUT_METHODS = {"value": _VALUE, "txt": _TXT, "voice": _VOICE, "txtvoice": _TXT_VOICE}
    _INPUT_SELECTED = 0
    _OUTPUT_SELECTED = 0
    '''
    Voice config
    '''
    _AUDIO_PLAYER = None
    _THRESHOLD = .5
    _PAUSE_THRESHOLD = 2000
    # Object of speech_recognition
    _recognizer_r = None
    # System program to play sounds
    _AUDIO_PLAYER = "mpg123"

    def __init__(self, audio_player, input_type="txt", output_type="txt"):
        self.set_input_method(input_type)
        self.set_audio_player(audio_player)
        self.set_output_method(output_type)

    '''
    Input configuration
    '''
    def set_input_method(self, input_type):
        try:
            self._INPUT_SELECTED = self._INPUT_METHODS[input_type]
        except KeyError:
            print(__class__.__name__ + ": Input method not exist")
            return False

    def get_input_method(self):
        return self._INPUT_SELECTED

    def listen(self):
        input_result = False

        # Expect a text input
        if self.get_input_method() == self._TXT:
            input_text = input("> ")
            input_result = input_text.lower()
        
        # Expect a audio input
        elif self.get_input_method() == self._VOICE:
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
        else:
            print("Not output method selected")

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
            print(__class__.__name__ + ": Output method not exist")
            return False
        if self.get_output_method() >= 2:
            self.set_voice_recognizer()
            

    def get_output_method(self):
        return self._OUTPUT_SELECTED

    def _set_ouput_limit(self, text):
        limit = min(100, len(text))  # 100 characters is the current limit.
        return text[0:limit]

    def _print_response(self, text):
        print("- Gozokia: ", self._set_ouput_limit(text))

    def response(self, text):
        if self.get_output_method() == self._VALUE:
            return text
        if self.get_output_method() == self._TXT or self.get_output_method() == self._TXT_VOICE:
            self._print_response(text)

        if self.get_output_method() >= 2:
            self._speak_response(text)
        return False
    '''
    Voice configuration
    '''
    def set_audio_player(self, audio_player):
        self._AUDIO_PLAYER = audio_player

    def set_language(self, lang):
        self._LANGUAGE = lang

    def get_language(self):
        return self._LANGUAGE

    def set_voice_recognizer(self):
        self._recognizer_r = sr.Recognizer(language=self.get_language())
        self._recognizer_r.dynamic_energy_threshold = True
        self._recognizer_r.energy_threshold = self._THRESHOLD
        self._recognizer_r.pause_threshold = .5


    def _speak_response(self, text, lang='es', fname='r.mp3', player=None):
        text = self._set_limit(text)
        """ 
        Sends text to Google's text to speech service
        and returns created speech (wav file). "
        """
        url = "http://translate.google.com/translate_tts"
        data = "?q=%s&textlen=%d&tl=%s&client=%s" % (text, len(text), lang, "t")
        url = url +data
        headers = {}
        headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        # TODO catch exceptions
        print(url)
        try:
            req = urllib.request.Request(url, headers = headers)
            p = urllib.request.urlopen(req)
        except Exception as e:
            print(str(e))
            return False
        f = open(fname, 'wb')
        f.write(p.read())
        f.close()
        self.__play_mp3('r.mp3')

    def __play_mp3(self, path):
        if self._AUDIO_PLAYER == 'mpg123':
            subprocess.Popen(['mpg123', '-q', path]).wait()
    '''
    def _is_magic_word(self, input_result):
        value = self._check_magic_word(input_result)
        if value is not False:
            self._OUTPUT_SELECTED = value
            if value == 0:
                self.response("Entendido, ahora te escribiré")
            elif value == 1:
                self.response("Entendido, ahora te hablaré")
            elif value == 2:
                self.response("Entendido, ahora te hablaré")
            elif value == 3:
                self.response("Entendido, ahora te escribiré y hablaré")
            return True
        return input_result
    '''
