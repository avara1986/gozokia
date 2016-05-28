# encoding: utf-8
"""
Gozokia model
"""
from __future__ import print_function

from abc import ABCMeta, abstractmethod


class ModelBase:
    __metaclass__ = ABCMeta
    """
    Metaclass for all models.
    """
    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_db(self):
        pass

    @abstractmethod
    def get(self, key=None, search=None):
        pass

    @abstractmethod
    def set_chat(self, user, session, text, type_rule, rule, status):
        pass

    @abstractmethod
    def get_chat(self, session, user=None):
        pass

    @abstractmethod
    def set(self, *args, **kwargs):
        pass
