# encoding: utf-8
"""
Core exceptions
"""


class GozokiaError(Exception):
    '''raise this when there's a lookup error for my app'''
    pass


class ImproperlyConfigured(Exception):
    pass
