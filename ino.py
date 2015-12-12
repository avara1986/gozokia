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
from command import CommandBase


class Io(CommandBase):

    """
    RESPONSES
    """
    _INPUT_METHODS = {"txt": 0, "voice": 1}
    _OUTPUT_METHODS = {"txt": 0, "voice": 1, "txtvoice": 2}
    _INPUT_SELECTED = 0
    _OUTPUT_SELECTED = 0
    _THRESHOLD = 2000
    _MAGIC_WORDS = {"h[á|a]blame": 1,
                    "escríbeme": 0,
                    "escr[i|í]beme": 0,
                    "escribiryhablar": 2,
                    "hablayescribe": 2,
                    "escribeyhabla": 2}
    """
    Object of speech_recognition
    """
    _recognizer_r = None
    """
    System program to play sounds
    """
    _AUDIO_PLAYER = "mpg123"

    def __init__(self, audio_player, input_type="txt", output_type="txt"):
        try:
            self.set_input_method(self._INPUT_METHODS[input_type])
        except KeyError:
            print(__class__.__name__ + ": Opción de entrada no existe")
            return False
        try:
            self._OUTPUT_SELECTED = self._OUTPUT_METHODS[output_type]
        except KeyError:
            print(__class__.__name__ + ": Opción de entrada no existe")
            return False
        self.AUDIO_PLAYER = audio_player
        self._recognizer_r = sr.Recognizer(language="es-ES")
        self._recognizer_r.dynamic_energy_threshold = True
        self._recognizer_r.energy_threshold = self._THRESHOLD
        self._recognizer_r.pause_threshold = .5

    def set_input_method(self, value):
        self._INPUT_SELECTED = value

    def _set_limit(self, text):
        limit = min(100, len(text))  # 100 characters is the current limit.
        return text[0:limit]

    def _print_response(self, text):
        print("- Gozokia: ", self._set_limit(text))

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
            f = open(fname, 'wb')
            f.write(p.read())
            f.close()
            self.__play_mp3('r.mp3')
        except Exception as e:
            print(str(e))


    def __play_mp3(self, path):
        if self._AUDIO_PLAYER == 'mpg123':
            subprocess.Popen(['mpg123', '-q', path]).wait()

    def _is_magic_word(self, input_result):
        value = self._check_magic_word(input_result)
        if value is not False:
            self._OUTPUT_SELECTED = value
            if value == 0:
                self.response("Entendido, ahora te escribiré")
            elif value == 1:
                self.response("Entendido, ahora te hablaré")
            elif value == 2:
                self.response("Entendido, ahora te escribiré y hablaré")
            return True
        return input_result

    def listen(self):
        input_result = False
        
        '''
        Expect a text input
        '''
        if self._INPUT_SELECTED == 0:
            input_text = input("> ")
            input_result = input_text.lower()
            '''
            Expect a audio input
            '''
        elif self._INPUT_SELECTED == 1:
            # use the default microphone as the audio source
            with sr.Microphone() as source:
                # listen for the first phrase and extract it into audio data
                input_audio = self._recognizer_r.listen(source)
            try:
                # print("You said " + r.recognize(audio))    # recognize speech
                # using Google Speech Recognition
                input_result = self._recognizer_r.recognize(input_audio).lower()
                input_result = input_result.encode('utf8')
            # speech is unintelligible
            except LookupError:
                print("No te entiendo")
                return False
        else:
            print("No se seleccionó ninguna opción de entrada")
        if len(input_result) == 0:
            input_result = False
        return self._is_magic_word(input_result)

    def response(self, text):
        if self._OUTPUT_SELECTED == 0 or self._OUTPUT_SELECTED == 2:
            self._print_response(text)

        if self._OUTPUT_SELECTED >= 1:
            self._speak_response(text)
