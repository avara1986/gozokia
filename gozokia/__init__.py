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
@goz.rule('foo', type=goz.RAISE_COND, rank=10)
class bar():
    completed = False

    @classmethod
    def condition(*args, **kwargs):
        sentence = kwargs.get('sentence')
        if len([True for t in sentence if t == ('foo', 'NN')]) > 0:
            return True

    @classmethod
    def response(cls, *args, **kwargs):
        cls.completed = True
        return ('bar')

    @classmethod
    def is_completed(cls, *args, **kwargs):
        return cls.completed
