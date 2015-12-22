# encoding: utf-8
import os
from gozokia.i_o import Io
from gozokia.conf import settings
from gozokia.core import Rule
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
    rules_map = Rule()
    '''
    GOZOKIA_DIR: The directory where gozokia have been calling.
    '''
    GOZOKIA_DIR = os.path.dirname(os.path.abspath(__file__))

    '''
    PROJECT_DIR: The directory where the project is running.
    '''
    PROJECT_DIR = os.getcwd()

    def __init__(self):
        if settings.DEBUG is True:
            print("Input selected: {}".format(settings.GOZOKIA_INPUT_TYPE))
            print("Output selected: {}".format(settings.GOZOKIA_OUTPUT_TYPE))
        self.set_io(input_type=settings.GOZOKIA_INPUT_TYPE,
                    output_type=settings.GOZOKIA_OUTPUT_TYPE,
                    )

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
        self.rules_map.add({rule: view_func})

    def console(self):
        input_result = True
        p = multiprocessing.Process(target=start_led)
        p.start()
        if settings.DEBUG is True:
            print("***** Activate rules *****")
            for rule in self.rules_map:
                print(rule)
        while input_result is not False:
            input_result = self.io.listen()

            # TODO: Get logic here
            output_result = "you said: {}".format(input_result)

            self.io.response(output_result)
        p.terminate()


