# encoding: utf-8
'''
Default settings of Gozokia.
Its coulds be defined on your Django settings
'''
from .gozokia import Gozokia

__author__ = "Alberto Vara"
__email__ = "a.vara.1986@gmail.com"
__version__ = "0.2"
__license__ = "MIT"

# Initialize
goz = Gozokia()


# Register our rules
@goz.rule('foo')
def bar():
    print('Hello')