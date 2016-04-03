# encoding: utf-8
import sys
import os
from gozokia import Gozokia
os.environ.setdefault("GOZOKIA_SETTINGS_MODULE", "settings")

goz = Gozokia()
goz.initialize()
goz.set_io(input_type="terminal_txt", output_type="terminal_txt")
goz.console()
