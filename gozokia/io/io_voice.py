import speech_recognition as sr

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
