# encoding: utf-8
from __future__ import absolute_import, print_function, unicode_literals
import sys

from gozokia.gozokia import Gozokia

print('aaa Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))
gozokia = Gozokia()
gozokia.set_io(input_type="value")
gozokia.set_io(input_type="terminal_txt", output_type="terminal_txt")
gozokia.console()
