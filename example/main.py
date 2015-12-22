#!/usr/bin/env python3
# encoding: utf-8
import os
import sys
sys.path.insert(0, os.getcwd())
from gozokia import Gozokia
from pymongo import MongoClient

# First, declare our settings file:
os.environ.setdefault("GOZOKIA_SETTINGS_MODULE", "settings")

# Initialize
goz = Gozokia()
# client = MongoClient("mongodb://192.168.100.7:27019")


# Register our rules
@goz.rule('test')
def my_function():
    print('Hello')

if __name__ == '__main__':
    print('\n*** Gozokia ***')
    '''
    # INPUT TYPE:
    goz.set_io(input_type="value")
    print(goz.io.listen(value="Hola hola!"))
    '''
    goz.console()
