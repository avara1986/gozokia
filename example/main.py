#!/usr/bin/env python3
# encoding: utf-8
import os
import sys
sys.path.insert(0, os.getcwd())
from gozokia import Gozokia
from gozokia.core.rules import RuleBase
from example.my_class import MyClassObjetive

# First, declare our settings file:
os.environ.setdefault("GOZOKIA_SETTINGS_MODULE", "settings")

# Initialize
goz = Gozokia()

# Register our class rules
goz.rule(type=goz.OBJETIVE_COND, rank=2)(MyClassObjetive)


# Register our class rules
@goz.rule(type=goz.RAISE_COND, rank=3)
class MyClass2(RuleBase):
    def condition(self, *args, **kwargs):
        return False

    def response(self, *args, **kwargs):
        return ('My Class2')

# Run Gozokia console
if __name__ == '__main__':
    goz.initialize()
    print('\n*** Gozokia ***')
    '''
    # INPUT TYPE:
    goz.set_io(input_type="value")
    print(goz.io.listen(value="Hola hola!"))
    '''
    goz.console()
