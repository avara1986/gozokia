# encoding: utf-8
from __future__ import unicode_literals
'''
Default settings of Gozokia.
Its coulds be defined on your Django settings
'''
from gozokia.app import Gozokia
from gozokia.rules import Bar
__author__ = "Alberto Vara"
__email__ = "a.vara.1986@gmail.com"
__version__ = "0.2"
__license__ = "MIT"

# Initialize
goz = Gozokia()


# Register our rules
goz.rule('foo', type=goz.RAISE_COND, rank=100)(Bar)
