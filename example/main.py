#!/usr/bin/env python3
# encoding: utf-8
import os
import sys
from pymongo import MongoClient
sys.path.insert(0, os.getcwd())
from gozokia import Gozokia
from example.my_class import MyClass

# First, declare our settings file:
os.environ.setdefault("GOZOKIA_SETTINGS_MODULE", "settings")

# Initialize
goz = Gozokia()
# client = MongoClient("mongodb://192.168.100.7:27019")


# Register our function rules
# @goz.rule('test_func')
def my_function():
    print('Hello function')

# Register our class rules
goz.rule('test_class')(MyClass)


# Register our class rules
@goz.rule('test_class2')
class MyClass2():
    def my_method(self):
        print('Hello method')

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
