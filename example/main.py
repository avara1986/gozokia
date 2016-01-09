#!/usr/bin/env python3
# encoding: utf-8
import os
import sys
# from pymongo import MongoClient
sys.path.insert(0, os.getcwd())
from gozokia import Gozokia
from example.my_class import MyClassObjetive

# First, declare our settings file:
os.environ.setdefault("GOZOKIA_SETTINGS_MODULE", "settings")

# Initialize
goz = Gozokia()
# client = MongoClient("mongodb://192.168.100.7:27019")

# Register our class rules
goz.rule('test_class', type=goz.OBJETIVE_COND, rank=2)(MyClassObjetive)


# Register our class rules
@goz.rule('test_class2', type=goz.RAISE_COND, rank=3)
class MyClass2():
    completed = False

    @classmethod
    def condition(cls, *args, **kwargs):
        return False

    @classmethod
    def response(cls, self, *args, **kwargs):
        return ('My Class2')

    @classmethod
    def is_completed(cls, *args, **kwargs):
        return cls.completed
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
