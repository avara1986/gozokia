#!/usr/bin/env python
# encoding: utf-8
import urllib2
import urllib
import speech_recognition as sr
import subprocess
import time
class Gozokia:
    def __init__(self):
        result = True
        while result != False:
            result = self.listen()
    def listen(self):
        r = sr.Recognizer(language = "es-ES")
        r.dynamic_energy_threshold = True
        r.energy_threshold = 4000
        with sr.Microphone() as source:                # use the default microphone as the audio source
            audio = r.listen(source)                   # listen for the first phrase and extract it into audio data
        try:
            #print("You said " + r.recognize(audio))    # recognize speech using Google Speech Recognition
            return self.get_response(r.recognize(audio))
        except LookupError:                            # speech is unintelligible
            print("Could not understand audio")
            return False
    def speak(self, text='hola', lang='es', fname='r.mp3', player=None):
        """ Sends text to Google's text to speech service
        and returns created speech (wav file). """
    
        limit = min(100, len(text))#100 characters is the current limit.
        text = text[0:limit]
        print "- Gozokia: ", text
        url = "http://translate.google.com/translate_tts"
        values = urllib.urlencode({"q": text, "textlen": len(text), "tl": lang})
        hrs = {"User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7"}
        #TODO catch exceptions
        req = urllib2.Request(url, data=values, headers=hrs)
        p = urllib2.urlopen(req)
        f = open(fname, 'wb')
        f.write(p.read())
        f.close()
        if player is not None:
            play_wav(fname, player)
    
    
    
    def play_mp3(self, path):
        subprocess.Popen(['mpg123', '-q', path]).wait()
    
    def get_response(self, response):
        response = response.encode('utf-8')
        print "+ Tú: ", response
        if response == 'Hola':
            self.speak(text='hola')
        elif response == 'qué tal':
            self.speak(text='bien, ¿y tu?')
        elif response == 'Alberto me quiere':
            self.speak(text='No te imaginas cuanto jijiji')
        elif response == 'mecagoentuputamadre':
            self.speak(text='y yo en la tuya jejeje')
        elif response == 'adios' or response == 'adiós':
            self.speak(text='Gero arté')
            return False
        else:
            self.speak(text='No te entiendo')
        self.play_mp3('r.mp3')
        return True

Gozokia()
