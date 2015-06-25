#!/usr/bin/env python
#-----------------------------------------------------
# Python 'Evolution of Text' Program
# More programs at: usingpython.com/programs
#-----------------------------------------------------
import pyaudio
import speech_recognition as sr

p = pyaudio.PyAudio()
        
r = sr.Recognizer(language = "es-ES", key = "AIzaSyCldaaMHWM80B43BQx4d2j0lil5rnX3JU4")
r.energy_threshold = 4000
r.pause_threshold = .5
with sr.Microphone() as source:                # use the default microphone as the audio source
    audio = r.listen(source, timeout=2)                   # listen for the first phrase and extract it into audio data

try:
    print("You said " + r.recognize(audio))    # recognize speech using Google Speech Recognition
except LookupError:                            # speech is unintelligible
    print("Could not understand audio")
    