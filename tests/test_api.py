# encoding: utf-8
import unittest
import os
from gozokia import Gozokia
from gozokia.rules import GreetingRaise, GreetingObjetive

os.environ.setdefault("GOZOKIA_SETTINGS_MODULE", "tests.settings_tests")


class ApiTest(unittest.TestCase):

    def test_foo(self):
        goz = Gozokia()
        goz.initialize()
        goz.set_io(input_type="value", output_type="value")
        value = "foo"
        self.assertEqual(goz.api(value), "bar")
        value = "foo"
        self.assertEqual(goz.api(value), "bar second")
        value = "foo"
        self.assertEqual(goz.api(value), "No rules. you said: foo")

    def test_greetings(self):
        goz = Gozokia()
        goz.rule(name='greeting', type=goz.RAISE_COND, rank=100)(GreetingRaise)
        goz.initialize()
        goz.set_io(input_type="value", output_type="value")
        value = "foo"
        self.assertEqual(goz.api(value), "bar")
        value = "Bacon"
        self.assertEqual(goz.api(value), "No rules. you said: Bacon")
        value = "Hi"
        self.assertEqual(goz.api(value), "Hi, who are you?")
        value = "i am Alberto"
        self.assertEqual(goz.api(value), "Hi, alberto")

if __name__ == '__main__':
    unittest.main()
