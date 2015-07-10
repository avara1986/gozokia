#!/usr/bin/env python
# encoding: utf-8

"""Library for personal assistans."""

__author__ = "Alberto Vara"
__version__ = "0.0.1"
__license__ = "MIT"

import re
from subprocess import call
from ino import Io

INPUT_TYPE = "txt"
OUTPUT_TYPE = "txtvoice"
AUDIO_PLAYER = 'mpg123'


class CommandSystem(Io):
    _MAGIC_WORDS = {"verficheros": 1,
                    "mail": 2, }

    def execute(self, input=""):
        if type(input) == str:
            return self._is_magic_word(input)
        return input

    def _is_magic_word(self, input):
        value = self._check_magic_word(input)
        if value is not False:
            if value == 1:
                call(["ls", "-l"])
            elif value == 2:
                self.send_mail()
            return False
        return input

    def send_mail(self):
        self.response(text='Dime asunto')
        asunto = self.listen()
        self.response(text='¿para quién?')
        para = self.listen()
        self.response(text='¿qué quieres enviar?')
        cuerpo = self.listen()
        import smtplib

        sender = 'a.vara@gobalo.es'
        receivers = [para]

        message = """From: Gozokia <a.vara@gobalo.es>
        To: To Person <%s>
        Subject: %s
        %s
        """
        message = message % (para, asunto, cuerpo)
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail(sender, receivers, message)
        print "Successfully sent email"
        return True


class Chat(Io):
    _MAGIC_WORDS = {"verficheros": 1,
                    "mail": 2, }

    def execute(self, input=""):
        # print "llega 3"
        # print type(input)
        if type(input) == str:
            return self.get_response(input)
        return input

    def get_response(self, response_input):

        print "+ Tú: ", response_input
        if response_input == 'hola':
            self.response(text='hola')
        elif response_input == 'qué tal':
            self.response(text='bien, ¿y tu?')
        elif response_input == 'alberto me quiere':
            self.response(text='No te imaginas cuanto jijiji')
        elif response_input == 'mecagoentuputamadre':
            self.response(text='y yo en la tuya jejeje')
        elif response_input == 'adios' or response_input == 'adiós':
            self.response(text='Gero arté')
            return False
        elif response_input == 'felicita a erik':
            self.response(text='¡Felicidades erik!')
        elif response_input == 'felicita a laura':
            self.response(text='Felicidades laura!')
        elif re.match(r'di (.)', response_input) is not None:
            self.response(
                re.search(r'di (?P<response>[\s\S]+)', response_input).group('response'))
        else:
            ##
            self.response(
                text='No te entiendo, ¿qué es %s?' % response_input)
        return True


class Gozokia:

    def __init__(self, input_type="txt"):
        self.ino = Io(
            input_type=INPUT_TYPE, output_type=OUTPUT_TYPE, audio_player=AUDIO_PLAYER)
        input = True
        self.cs = CommandSystem(
            input_type=INPUT_TYPE, output_type=OUTPUT_TYPE, audio_player=AUDIO_PLAYER)
        self.chat = Chat(
            input_type=INPUT_TYPE, output_type=OUTPUT_TYPE, audio_player=AUDIO_PLAYER)
        while input != False:
            input = self.ino.listen()
            input = self.cs.execute(input)
            input = self.chat.execute(input)

if __name__ == '__main__':
    print '\n*** Gozokia ***'
    Gozokia()
