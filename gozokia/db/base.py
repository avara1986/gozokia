'''
Gozokia model
based on Django settings module:
https://github.com/django/django/blob/master/django/conf/__init__.py
'''
import os
import importlib
from gozokia.conf import settings


class ModelBase(object):
    """
    Metaclass for all models.
    """
    def __init__(self, *args, **kwargs):
        mod = importlib.import_module(settings.DATABASES['default']['ENGINE'])
        self.db = mod.Database()

    def get_db(self):
        return self.db

    def get(self, key=None):
        return self.db.get(key)

    def set_chat(self, chat):
        self.db.set({'chat': chat})

    def set(self, *args, **kwargs):
        return self.db.set(*args, **kwargs)
