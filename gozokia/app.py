# encoding: utf-8
import os
import datetime
import time
import multiprocessing

from gozokia.i_o import Io
from gozokia.conf import settings
from gozokia.core import Rules
from gozokia.core.text_processor import Analyzer
from gozokia.db.base import ModelBase

# settings.configure()


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

    def initialize(self):
        if settings.DEBUG is True:
            print("Input selected: {}".format(settings.GOZOKIA_INPUT_TYPE))
            print("Output selected: {}".format(settings.GOZOKIA_OUTPUT_TYPE))
        self.set_io(input_type=settings.GOZOKIA_INPUT_TYPE,
                    output_type=settings.GOZOKIA_OUTPUT_TYPE,
                    )
        self.analyzer = Analyzer()
        self.db = ModelBase()

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

    def eval(self, sentence):
        self.analyzer.set(sentence)
        rule = self.rules.get_rule(self, self.analyzer)
        if rule is not None:
            rule_object = rule["class"]
            response = rule_object.response()
        else:
            response = "you said: {}".format(sentence)
            rule = 'Gozokia'

        self.db.set_chat({'timestamp': datetime.datetime.now(), 'text': response, 'type': 'O', 'rule': str(rule)})
        return response

    def console(self):
        input_result = True
        p = multiprocessing.Process(target=start_led)
        p.start()
        while input_result is not False:
            input_result = self.io.listen()
            if input_result:
                self.db.set_chat({'timestamp': datetime.datetime.now(), 'text': input_result, 'type': 'I'})
                output_result = self.eval(input_result)
                print(self.analyzer.get_tagged())
                self.io.response(output_result)
        print(self.db.get())
        p.terminate()


