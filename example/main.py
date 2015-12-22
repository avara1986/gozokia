#!/usr/bin/env python3
# encoding: utf-8
import os
import sys
from pymongo import MongoClient

sys.path.insert(0, os.getcwd())
from gozokia import Gozokia


# First, declare our settings file:
os.environ.setdefault("GOZOKIA_SETTINGS_MODULE", "settings")

# Initialize
goz = Gozokia()
# client = MongoClient("mongodb://192.168.100.7:27019")


# Register our rules
@goz.rule('test_func')
def my_function():
    print('Hello function')


# Register our rules
@goz.rule('test_class')
class my_class():
    def my_method(self):
        print('Hello method')

if __name__ == '__main__':
    goz.initialize()
    print('\n*** Gozokia ***')
    '''
    # INPUT TYPE:
    goz.set_io(input_type="value")
    print(goz.io.listen(value="Hola hola!"))
    '''
    goz.console()
