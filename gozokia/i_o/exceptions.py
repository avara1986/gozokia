# encoding: utf-8
"""
I/O exceptions
"""


class GozokiaIoError(Exception):
    '''raise this when there's a lookup error for my app'''
    pass


class GozokiaOutputError(GozokiaIoError):
    '''raise this when there's a lookup error for my app'''
    pass
