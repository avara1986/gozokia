# encoding: utf-8
from __future__ import unicode_literals
'''
Default settings of Gozokia.
Its coulds be defined on your Django settings
'''
from gozokia.app import Gozokia

__author__ = "Alberto Vara"
__email__ = "a.vara.1986@gmail.com"
__version__ = "0.2"
__license__ = "MIT"

# Initialize
goz = Gozokia()


# Register our rules
@goz.rule('foo', type="rise")
class bar():
    def condition(self, *args, **kwargs):
        sentence = kwargs.get('sentence')
        if sentence == "bar":
            return True

    def response(self, *args, **kwargs):
        return ('foo')
