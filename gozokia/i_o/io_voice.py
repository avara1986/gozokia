import os
import speech_recognition as sr
import urllib.request
import urllib.parse
import subprocess
from .io_base import GozokiaIoError
r = sr.Recognizer()
m = sr.Microphone()


class VoiceRecognizerMixin(object):
        # Object of speech_recognition
    _recognizer_r = None
    '''
    Voice config
    '''
    _THRESHOLD = .8
    _PAUSE_THRESHOLD = 4000

    def set_voice_recognizer(self):
        pass
        # r = sr.Recognizer()
        # r.dynamic_energy_threshold = True
        # r.energy_threshold = self._THRESHOLD
        # r.pause_threshold = self._THRESHOLD

    def listen_audio(self, language):
        # use the default microphone as the audio source
        with m as source:
            r.adjust_for_ambient_noise(source)
            print("Set minimum energy threshold to {}".format(r.energy_threshold))
            # listen for the first phrase and extract it into audio data
            input_audio = r.listen(source)
            print("Got it! Now to recognize it...")
            try:
                # using Google Speech Recognition
                input_result = r.recognize_google(input_audio, language=language)
                if str is bytes:  # this version of Python uses bytes for strings (Python 2)
                    input_result = input_result.encode('utf8')
            except sr.UnknownValueError:
                input_result = ("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                input_result = ("Could not request results from Google Speech Recognition service; {0}".format(e))
            # speech is unintelligible
            except LookupError:
                input_result = ("I don't understand you")
        return input_result


class VoiceResponseMixin(object):

    def _set_ouput_limit(self, text):
        limit = min(100, len(text))  # 100 characters is the current limit.
        return text[0:limit]

    def response_speak(self, text, language):
        fname = 'r.mp3'
        text = self._set_ouput_limit(text)
        """
        Sends text to Google's text to speech service
        and returns created speech (wav file). "
        """
        url = "http://translate.google.com/translate_tts"
        # data = "?q=%s&textlen=%d&tl=%s&client=%s" % (text, len(text), language, "t")
        data = urllib.parse.urlencode({'key': os.environ.get('GOOGLE_TRANSLATE_KEY'),
                                       "q": text,
                                       "textlen": len(text),
                                       "tl": language,
                                       "client": "t"})
        url = url + "?" + data
        headers = {}
        headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        # TODO catch exceptions
        try:
            req = urllib.request.Request(url, headers=headers)
            p = urllib.request.urlopen(req)
        except Exception as e:
            raise GozokiaIoError(__class__.__name__ + ": Error on voice: {}".format(str(e)))
        f = open(fname, 'wb')
        f.write(p.read())
        f.close()
        self.__play_mp3('r.mp3')

    def __play_mp3(self, path):
        if os.environ.get('GOZOKIA_AUDIO_PLAYER') == 'mpg123':
            subprocess.Popen(['mpg123', '-q', path]).wait()
        else:
            raise GozokiaIoError(__class__.__name__ + ": No sound player selected")
