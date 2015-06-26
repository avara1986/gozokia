# encoding: utf-8
"""Library for personal assistans."""

__author__ = "Alberto Vara"
__version__ = "0.0.1"
__license__ = "MIT"

import re
import abc


class CommandBase(object):
    __metaclass__ = abc.ABCMeta
    _MAGIC_WORDS = {}

    def __init__(self):
        pass

    def _findWholeWord(self, w):
        return re.compile(r'({0})'.format(w), flags=re.IGNORECASE).search

    def _check_magic_word(self, input):
        if isinstance(input, str):
            for (word, value) in self._MAGIC_WORDS.items():
                match = self._findWholeWord(word)(input.replace(" ", ""))
                if match is not None:
                    return value
        return False
