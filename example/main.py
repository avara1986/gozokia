#!/usr/bin/env python
# encoding: utf-8
import os
import sys
sys.path.insert(0, os.getcwd())

from gozokia import Gozokia

if __name__ == '__main__':
    print('\n*** Gozokia ***')
    gozokia = Gozokia()
    gozokia.console()