# encoding: utf-8
import multiprocessing
import os
import re
import uuid
import time

from gozokia.i_o import Io
from gozokia.conf import settings
from gozokia.core import Rules
from gozokia.core.text_processor import Analyzer
from gozokia.utils.util_logging import Logging
from gozokia.db import Model

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
    rules = None
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

    _no_rule = {'rule': "Gozokia", 'status': 0}

    def __init__(self, * args, **kwargs):
        session = kwargs.get('session', False)
        if session:
            self.session_id = session
        else:
            self.session_id = uuid.uuid1()
        user = kwargs.get('user', False)
        if user:
            self.user_id = user
        else:
            self.user_id = None
        self.rules = Rules(sessionid=self.session_id)

    def initialize(self, * args, **kwargs):
        # Set the text analyzer. Default nltk (http://www.nltk.org/)
        self.analyzer = Analyzer()

        # Set the model. Default nltk (http://www.nltk.org/)
        model = kwargs.get('model', False)
        self.db = model if model else Model()

        # Initialize the logger
        self.logger = Logging(__name__)
        self.logger.debug("DB selected: {}".format(settings.DATABASES['default']['ENGINE']))
        self.logger.debug("Input selected: {}".format(settings.GOZOKIA_INPUT_TYPE))
        self.logger.debug("Output selected: {}".format(settings.GOZOKIA_OUTPUT_TYPE))

        # Initialize the i/o methods. Default input text and output text
        self.set_io(input_type=settings.GOZOKIA_INPUT_TYPE,
                    output_type=settings.GOZOKIA_OUTPUT_TYPE,
                    )

    def set_io(self, *args, **kwargs):
        self.io = Io(*args, **kwargs)

    def rule(self, **options):
        """A decorator that is used to register a class for a
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
        rule = self._no_rule
        if self.sentence:
            sentence = self.sentence.lower()
            if sentence.startswith('gozokia'):
                if re.search("stop rule", sentence):
                    rule = self.rules.get_active_rule()
                    if rule is not None:
                        rule["class"].set_completed()
                        self.rules.stop_active_rule()
                        return "Stoped {}".format(str(rule['rule'])), rule
                elif re.search("thanks|thank you", sentence):
                    return "Your welcome", rule
                elif re.search("bye|exit|shutdown", sentence):
                    return "Bye", rule
        return False, rule

    def retrospective(self):
        """
        Initialize the rules based on old chats of the session or the user
        """
        chat_history = self.db.get_chat(session=self.session_id, user=self.user_id)
        print(chat_history)
        for chat in chat_history:
            if chat.type_rule == 'O':
                for r in self.rules.get_rules():
                    if r['rule'] == chat.rule:
                        if chat.status == self.rules._STATUS_RULE_ACTIVE:
                            self.rules.set_active_rule(r)
                        elif chat.status == self.rules._STATUS_RULE_PENDING:
                            self.rules.set_rule_pending(r)
                        elif chat.status == self.rules._STATUS_RULE_COMPLETED:
                            self.rules.set_rule_completed(r)

    def eval(self, sentence):
        """
        Params:
        sentence: sting

        return:
        response_output: string. the response to send to the IO output
        print_output: string. The response to print, no parsed on IO output
        """
        print_output = None
        self.sentence = sentence
        self.analyzer.set(sentence)

        # Add the input to DDBB
        self.db.set_chat(**{'user': self.user_id, 'session': self.session_id,
                            'text': self.sentence, 'type_rule': 'I',
                            'rule': None, 'status': None})
        self.retrospective()
        response_output, rule = self.check_system_rules()
        if not response_output:
            # Check rules:
            rule, response_output, print_output = self.rules.eval(self)
            if not rule:
                # Default "no rules"
                response_output = "No rules. you said: {}".format(sentence)
                rule = self._no_rule

        # Add the output to DDBB
        self.db.set_chat(**{'user': self.user_id, 'session': self.session_id,
                            'text': response_output, 'type_rule': 'O',
                            'rule': rule['rule'], 'status': rule['status']})

        return response_output, print_output

    def get_response(self, input_result):
        """

        """
        output_result = ""
        print_output = ""

        if input_result:
            output_result, print_output = self.eval(input_result)
            self.logger.debug(self.analyzer.get_tagged())
            if print_output:
                self.logger.debug(print_output)
            return self.io.response(output_result)

        return None

    def console(self):
        """
        The api method's designed to run in console
        method works with the settings:
        GOZOKIA_INPUT_TYPE = "terminal_txt" or GOZOKIA_INPUT_TYPE = "terminal_voice"
        """
        output_result = True
        p = multiprocessing.Process(target=start_led)
        p.start()
        while output_result != "Bye":
            output_result = self.get_response(self.io.listen())
            print(output_result)

        self.logger.debug(self.db.get())
        p.terminate()

    def api(self, input_result):
        """
        The api methods designed to receive a value and parse. This
        method works with the settings:
        GOZOKIA_INPUT_TYPE = "value"
        ------------------------------------------------------------
        self.io.listen return a string
        """
        return self.get_response(input_result=self.io.listen(value=input_result))
