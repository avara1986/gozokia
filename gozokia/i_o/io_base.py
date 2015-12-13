# encoding: utf-8
"""
I/O configurations
"""


class GozokiaIoError(Exception):
    '''raise this when there's a lookup error for my app'''


class InputBase(object):

    def __init__(self, *args, **kwargs):
        pass

    def listen(self, *args, **kwargs):
        pass


class OutputBase(object):

    def __init__(self, *args, **kwargs):
        pass

    def response(self, *args, **kwargs):
        pass
