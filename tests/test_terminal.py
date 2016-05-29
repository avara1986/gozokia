# encoding: utf-8
import unittest
import os
from gozokia import Gozokia

os.environ.setdefault("GOZOKIA_SETTINGS_MODULE", "tests.settings_tests")


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


if __name__ == '__main__':
    unittest.main()
