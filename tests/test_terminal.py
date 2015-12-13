# encoding: utf-8
import unittest
from time import sleep
import os
import random
import sys

sys.path.insert(0, os.getcwd())

from gozokia.gozokia import Gozokia


class TerminalTest(unittest.TestCase):

    def test_text(self):
        gozokia = Gozokia()
        value = "Hello world"
        '''
        self.assertEqual(gozokia.i_o.listen(), value)
        gozokia.set_io(input_type="terminal_txt", output_type="terminal_txt")
        value = "Hello world I: terminal_txt O: terminal_txt"
        self.assertEqual(gozokia.i_o.listen(), value)
        '''

    def test_input_text_output_text(self):
        pass


class ValueTest(unittest.TestCase):
    def test_value(self):
        gozokia = Gozokia()
        gozokia.set_io(input_type="value")
        value = "Hola hola!"
        self.assertEqual(gozokia.io.listen(value=value), value)

if __name__ == '__main__':
    unittest.main()