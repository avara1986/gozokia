#!/usr/bin/env python
# encoding: utf-8
import os
import sys
sys.path.insert(0, os.getcwd())
from gozokia.gozokia import Gozokia

if __name__ == '__main__':
    print('\n*** Gozokia ***')
    gozokia = Gozokia()
    gozokia.set_io(input_type="value")
    print(gozokia.io.listen(value="Hola hola!"))
    gozokia.set_io(input_type="terminal_txt", output_type="terminal_txt")
    gozokia.console()
