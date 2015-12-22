# encoding: utf-8
import sys
import os
from . import Gozokia
os.environ.setdefault("GOZOKIA_SETTINGS_MODULE", "settings")
print('aaa Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))

goz = Gozokia()
goz.initialize()
goz.set_io(input_type="terminal_txt", output_type="terminal_txt")
goz.console()
