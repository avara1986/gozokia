#!/usr/bin/env python3
# encoding: utf-8
import os
import sys
sys.path.insert(0, os.getcwd())
from gozokia.gozokia import Gozokia
from pymongo import MongoClient


client = MongoClient("mongodb://192.168.100.7:27019")


if __name__ == '__main__':
    os.environ.setdefault("GOZOKIA_SETTINGS_MODULE", "settings")
    print('\n*** Gozokia ***')
    gozokia = Gozokia()
    gozokia.set_io(input_type="value")
    print(gozokia.io.listen(value="Hola hola!"))
    gozokia.set_io(input_type="terminal_txt", output_type="terminal_txt")
    gozokia.console()
