# encoding: utf-8
import unittest
import os
from gozokia import Gozokia

os.environ.setdefault("GOZOKIA_SETTINGS_MODULE", "settings_tests")


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


class ApiTest(unittest.TestCase):

    def test_value(self):
        goz = Gozokia()
        goz.initialize()
        goz.set_io(input_type="value", output_type="value")
        value = "foo"
        self.assertEqual(goz.api(value), "bar")
        value = "foo"
        self.assertEqual(goz.api(value), "bar second")
        value = "foo"
        self.assertEqual(goz.api(value), "No rules. you said: foo")

if __name__ == '__main__':
    unittest.main()
