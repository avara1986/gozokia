#!/usr/bin/env python3
# encoding: utf-8
import os
import sys
sys.path.insert(0, os.getcwd())
from gozokia import Gozokia
# First, declare our settings file:
os.environ.setdefault("GOZOKIA_SETTINGS_MODULE", "settings")

# Initialize
goz = Gozokia()

# Run Gozokia console
if __name__ == '__main__':
    goz.initialize()
    input = "qwerty"
    goz.api(input)
    input = "alberto"
    goz.api(input)
    input = "foo"
    goz.api(input)
    input = "foo"
    goz.api(input)
    input = "foo"
    goz.api(input)
