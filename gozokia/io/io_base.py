# encoding: utf-8
"""
I/O base
"""
import abc

class InputBase(object):
    __metaclass__ = abc.ABCMeta
    def __init__(self):
        pass
    
    def listen(self, *args, **kwargs):
        pass

class OutputBase(object):
    __metaclass__ = abc.ABCMeta
    def __init__(self):
        pass
    
    def response(self, *args, **kwargs):
        pass