# encoding: utf-8
import os
from gozokia.i_o import Io
from gozokia.conf import settings
from gozokia.core import Rules
from gozokia.core.text_processor import Analyzer
from gozokia.db.base import ModelBase

import time
import multiprocessing


def start_led():
    '''
    if the console is running on a RaspberryPi, run a led
    '''
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
    rules_map = Rules()

    io = None
    '''
    GOZOKIA_DIR: The directory where gozokia have been calling.
    '''
    GOZOKIA_DIR = os.path.dirname(os.path.abspath(__file__))

    '''
    PROJECT_DIR: The directory where the project is running.
    '''
    PROJECT_DIR = os.getcwd()

    RAISE_COND = "raise"

    OBJETIVE_COND = "objetive"

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

    def set_io(self, *args, **kwargs):
        self.io = Io(*args, **kwargs)

    def rule(self, rule, **options):
        """A decorator that is used to register a view function for a
        given rule.
        """
        def decorator(f):
            self.add_rule(rule, f, **options)
            return f
        return decorator

    def add_rule(self, rule, view_func=None, **options):
        rank = 10
        type_rule = None
        if 'rank' in options and type(options['rank']) is int:
            rank = options['rank']
        if 'type' in options and type(options['type']) is str:
            type_rule = options['type']
        self.rules_map.add({'rule': rule, 'class': view_func, 'rank': rank, 'type': type_rule})

    def eval(self, sentence):
        self.analyzer.set(sentence)
        response = None
        tags = self.analyzer.get_tagged()
        for r in self.rules_map.get_raises():
            r_class = r['class']
            if r_class.condition(gozokia=self, sentence=tags):
                response = r_class.response()
                break
        for r in self.rules_map.get_raises():
            r_class = r['class']
            if r_class.is_completed():
                self.rules_map.pop(r)
        return response

    def console(self):
        input_result = True
        p = multiprocessing.Process(target=start_led)
        p.start()
        db = ModelBase()
        '''
        if settings.DEBUG is True:
            print("***** Activated rules *****")
            for rule in self.rules_map:
                print(rule)
            print("***** Activated raises *****")
            for rule in self.rules_map.get_raises():
                print(rule)
            print("***** Activated objectives *****")
            for rule in self.rules_map.get_objetives():
                print(rule)
        '''
        while input_result is not False:
            input_result = self.io.listen()
            if input_result:
                db.set({'text': input_result, 'type': 'I'})
                output_result = self.eval(input_result)
                # print(output_result)
                # TODO: Get logic here
                print(self.analyzer.get_tagged())
                if output_result == None:
                    output_result = "you said: {}".format(input_result)
                db.set({'text': output_result, 'type': 'O'})
                self.io.response(output_result)
        print(db.get())
        p.terminate()


