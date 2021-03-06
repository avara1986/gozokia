#!/usr/bin/env python3
# encoding: utf-8
from __future__ import absolute_import, print_function, unicode_literals
import os

from gozokia import Gozokia
from gozokia.core.rules import RuleBase
from gozokia.rules import GreetingRaise, GreetingObjetive
from my_class import MyClassObjetive
# First, declare our settings file:
os.environ.setdefault("GOZOKIA_SETTINGS_MODULE", "settings")

# Initialize
goz = Gozokia()

# Register our class rules
goz.rule(type=goz.OBJETIVE_COND, rank=2)(MyClassObjetive)
#goz.rule(name='greeting', type=goz.OBJETIVE_COND, rank=1)(Greeting)
goz.rule(name='greeting', type=goz.RAISE_COND, rank=100)(GreetingRaise)
# Register our class rules


@goz.rule(type=goz.RAISE_COND, rank=3)
class MyClass2(RuleBase):

    def condition_raise(self, *args, **kwargs):
        return False

    def response(self, *args, **kwargs):
        self.response_output = 'My Class2'

# Run Gozokia console
if __name__ == '__main__':
    goz.initialize()
    print('\n*** Gozokia ***')
    goz.console()
