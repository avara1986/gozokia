# encoding: utf-8
import unittest
from time import sleep
import os
import random

from gozokia import Gozokia


class TerminalTest(unittest.TestCase):

    def test_value(self):
        gozokia = Gozokia()
        gozokia.set_io(input_type="value")
        value = "Hola hola!"
        self.assertEqual(gozokia.io.listen(value=value), value)

    def test_input_text_output_text(self):
        pass
if __name__ == '__main__':
    unittest.main()