# encoding: utf-8
import unittest
import os
from gozokia import Gozokia

os.environ.setdefault("GOZOKIA_SETTINGS_MODULE", "tests.settings_tests")


class ValueTest(unittest.TestCase):

    def test_value(self):
        gozokia = Gozokia()
        gozokia.set_io(input_type="value")
        value = "Hola hola!"
        self.assertEqual(gozokia.io.listen(value=value), value)

if __name__ == '__main__':
    unittest.main()
