# encoding: utf-8
"""Library for personal assistans."""

__author__ = "Alberto Vara"
__version__ = "0.0.1"
__license__ = "MIT"

import re
import speech_recognition as sr
import subprocess
import urllib2
import urllib
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
            print __class__.__name__ + ": Opción de entrada no existe"
            return False
        try:
            self._OUTPUT_SELECTED = self._OUTPUT_METHODS[output_type]
        except KeyError:
            print __class__.__name__ + ": Opción de entrada no existe"
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
        print "- Gozokia: ", self._set_limit(text)

    def _speak_response(self, text, lang='es', fname='r.mp3', player=None):
        text = self._set_limit(text)
        """ Sends text to Google's text to speech service
        and returns created speech (wav file). """
        url = "http://translate.google.com/translate_tts"
        values = urllib.urlencode(
            {"q": text, "textlen": len(text), "tl": lang})
        hrs = {
            "User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7"}
        # TODO catch exceptions
        req = urllib2.Request(url, data=values, headers=hrs)
        p = urllib2.urlopen(req)
        f = open(fname, 'wb')
        f.write(p.read())
        f.close()
        self.__play_mp3('r.mp3')

    def __play_mp3(self, path):
        if self._AUDIO_PLAYER == 'mpg123':
            subprocess.Popen(['mpg123', '-q', path]).wait()

    def _is_magic_word(self, input):
        value = self._check_magic_word(input)
        if value is not False:
            self._OUTPUT_SELECTED = value
            if value == 0:
                self.response("Entendido, ahora te escribiré")
            elif value == 1:
                self.response("Entendido, ahora te hablaré")
            elif value == 2:
                self.response("Entendido, ahora te escribiré y hablaré")
            return True
        return input

    def listen(self):
        input = False
        if self._INPUT_SELECTED == 0:
            input_text = raw_input("> ")
            input = input_text.lower()
        elif self._INPUT_SELECTED == 1:
            # use the default microphone as the audio source
            with sr.Microphone() as source:
                # listen for the first phrase and extract it into audio data
                input_audio = self._recognizer_r.listen(source)
            try:
                # print("You said " + r.recognize(audio))    # recognize speech
                # using Google Speech Recognition
                input = self._recognizer_r.recognize(input_audio).lower()
                input = input.encode('utf8')
            # speech is unintelligible
            except LookupError:
                print("No te entiendo")
                return False
        else:
            print "No se seleccionó ninguna opción de entrada"
        if len(input) == 0:
            input = False
        return self._is_magic_word(input)

    def response(self, text):
        if self._OUTPUT_SELECTED == 0 or self._OUTPUT_SELECTED == 2:
            self._print_response(text)

        if self._OUTPUT_SELECTED >= 1:
            self._speak_response(text)
