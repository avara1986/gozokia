# encoding: utf-8
import os
import datetime
import time
import multiprocessing
import re

from gozokia.i_o import Io
from gozokia.conf import settings
from gozokia.core import Rules
from gozokia.core.text_processor import Analyzer
from gozokia.utils.util_logging import Logging
from gozokia.db.base import ModelBase

# settings.configure()

# https://github.com/nltk/nltk/blob/develop/nltk/chat/util.py
#chat = nltk.chat.util.Chat([(r'I like (.*)', ['Why do you like %1', 'Did you ever dislike %1']),], reflections)


def start_led():
    """
    if the console is running on a RaspberryPi, run a led
    """
    try:
        import RPi.GPIO as GPIO
    except ImportError:
        return False
    # Configure the Pi to use the BCM (Broadcom) pin names, rather than the pin positions
    GPIO.setmode(GPIO.BCM)

    red_pin = 18

    GPIO.setup(red_pin, GPIO.OUT)

    try:
        while True:
            GPIO.output(red_pin, True)  # LED on
            time.sleep(0.5)  # delay 0.5 seconds
            GPIO.output(red_pin, False)  # LED off
            time.sleep(0.5)  # delay 0.5 seconds
    finally:
        GPIO.cleanup()


class Gozokia:
    """
    Queue of rules
    """
    rules = Rules()
    """
    Text analyzer controller
    """
    analyzer = None
    """
    Input/Output controller
    """
    io = None
    """
    GOZOKIA_DIR: The directory where gozokia have been calling.
    """
    GOZOKIA_DIR = os.path.dirname(os.path.abspath(__file__))

    """
    PROJECT_DIR: The directory where the project is running.
    """
    PROJECT_DIR = os.getcwd()

    RAISE_COND = 1

    OBJETIVE_COND = 2

    def __init__(self):
        pass

    def initialize(self, * args, **kwargs):
        self.analyzer = Analyzer()
        model = kwargs.get('port', False)
        self.db = model if model else ModelBase()
        self.logger = Logging(__name__)
        self.logger.debug("Input selected: {}".format(settings.GOZOKIA_INPUT_TYPE))
        self.logger.debug("Output selected: {}".format(settings.GOZOKIA_OUTPUT_TYPE))
        self.set_io(input_type=settings.GOZOKIA_INPUT_TYPE,
                    output_type=settings.GOZOKIA_OUTPUT_TYPE,
                    )

    def set_io(self, *args, **kwargs):
        self.io = Io(*args, **kwargs)

    def rule(self, **options):
        """A decorator that is used to register a view function for a
        given rule.
        """
        def decorator(rule_class):
            self.__add_rule(rule_class, **options)
            return rule_class
        return decorator

    def __add_rule(self, rule_class, **options):
        self.rules.add(rule_class, **options)

    def check_system_rules(self):
        """
        System rules are the core rules. 
        """
        rule = "Gozokia"
        if self.sentence:
            sentence = self.sentence.lower()
            if sentence.startswith('gozokia'):
                if re.search("stop rule", sentence):
                    rule = self.rules.get_active_rule()
                    if rule is not None:
                        rule["class"].set_completed()
                        self.rules.set_active_rule(None)
                        return "Stoped {}".format(str(rule['rule'])), rule
                elif re.search("thanks|thank you", sentence):
                    return "Your welcome", rule
                elif re.search("bye|exit|shutdown", sentence):
                    return "Bye", rule
        return False, rule

    def eval(self, sentence):
        """
        Params:
        sentence: sting

        return:
        response_output: string. the response to send to the IO output
        print_output: string. The response to print, no parsed on IO output
        """
        response_output = None
        print_output = None
        self.sentence = sentence
        self.analyzer.set(sentence)

        # Add the input to DDBB
        self.db.set_chat(chat={'timestamp': datetime.datetime.now(), 'text': self.sentence, 'type': 'I'})

        response_output, rule = self.check_system_rules()
        if not response_output:
            # Check rules:
            rule = self.rules.get_rule(self)
            if rule is not None:
                rule_object = rule["class"]
                response_output, print_output = rule_object.get_response()
            else:
                response_output = "No rules. you said: {}".format(sentence)
                rule = 'Gozokia'

        # Add the output to DDBB
        self.db.set_chat(chat={'timestamp': datetime.datetime.now(), 'text': response_output, 'type': 'O', 'rule': str(rule)})

        return response_output, print_output

    def get_response(self, input_result):
        """

        """
        output_result = ""
        print_output = ""

        if input_result:
            output_result, print_output = self.eval(input_result)
            self.logger.debug(self.analyzer.get_tagged())
            self.io.response(output_result)
        if print_output:
            self.logger.debug(print_output)

        # TODO: Parse the output
        return output_result

    def console(self):
        output_result = True
        p = multiprocessing.Process(target=start_led)
        p.start()
        while output_result != "Bye":
            output_result = self.get_response(self.io.listen())
        if settings.DEBUG:
            self.logger.debug(self.db.get())
        p.terminate()

    def api(self, input_result):
        return self.get_response(input_result)
