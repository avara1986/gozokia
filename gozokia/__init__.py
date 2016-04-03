# encoding: utf-8
from __future__ import unicode_literals
"""
Default settings of Gozokia.
Its coulds be defined on your Django settings
"""
from gozokia.app import Gozokia
from gozokia.rules import Bar, BarSecond, Debug, Greeting
__author__ = "Alberto Vara"
__email__ = "a.vara.1986@gmail.com"
__version__ = "0.2"
__license__ = "MIT"

# Initialize
goz = Gozokia()


# Register our rules
goz.rule(name='foo', type=goz.RAISE_COND, rank=99)(Bar)
goz.rule(name='foosecond', type=goz.RAISE_COND, rank=100)(BarSecond)
goz.rule(name='debug', type=goz.RAISE_COND, rank=100)(Debug)
goz.rule(name='greeting', type=goz.OBJETIVE_COND, rank=100)(Greeting)
